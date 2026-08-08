# ReAct · Module 3: Workflow, stop conditions, System Prompt

> **Core reference · Module 3** (depends on [Module 1](./01-module-1-background-cross-dept-features-tone.md) · [Module 2](./02-module-2-department-toolbox.md))  
> LLM: **DeepSeek** (OpenAI-compatible API) · key only via env var `DEEPSEEK_API_KEY`; never commit to repo  
> Version: V1.0 · 2026-08-02

---

## 1. Workflow (unified control loop)

All department Skills **share** the same ReAct loop; variance is only in System Prompt slots and `allowed_tools`.

```text
Input (skill_id + user_input + optional customer_id/vin)
        │
        ▼
┌───────────────────┐
│ Load Skill config  │  YAML: tone / goal / stop / tool allowlist
│ Build System Prompt│  Base prompt + dept tone + tool instructions
└─────────┬─────────┘
          ▼
┌───────────────────┐
│  LLM (DeepSeek)    │  messages + tools (JSON Schema)
└─────────┬─────────┘
          │
     ┌────┴────┐
     │         │
  tool_calls  plain-text final answer
     │         │
     ▼         ▼
┌──────────────────┐
│ ToolRegistry.call │  Act + Observe
└─────────┬────────┘
          │ observation appended to messages; step += 1
          └──────► back to LLM (until stop)
```

### 1.1 Single-step semantics

| Step | Name | Who | Output |
|------|------|-----|--------|
| Think | Reason | DeepSeek | `tool_calls` or final natural language |
| Act | Action | `ToolRegistry` | `ToolResult` |
| Observe | Observe | Control loop | Append result to next user/tool message |

### 1.2 Code entry points

| Path | Responsibility |
|------|----------------|
| `shared/llm/client.py` | DeepSeek client |
| `agents/react/agent.py` | ReAct control loop |
| `skills/<id>/skill.yaml` | Goal / tone / stop / tool allowlist |
| `apps/cli.py --agent-type react` | Unified entry |

```bash
export DEEPSEEK_API_KEY=...   # or write to local .env (gitignored)
python apps/cli.py --agent-type react --skill fill_ticket \
  --input data/seeds/story_1_fill_ticket.json
```

---

## 2. Stop conditions

### 2.1 Global stops (all Skills)

| Condition ID | Trigger | Behavior |
|--------------|---------|----------|
| `S-MAX-STEPS` | `step >= max_steps` (default 8) | Force end; return collected evidence + `stop_reason=max_steps` |
| `S-FINAL` | Model returns text only, no tool_calls this turn | Normal end, `stop_reason=final` |
| `S-TOOL-DENY` | 2 consecutive `TOOL_NOT_ALLOWED` | End with permission hint, `stop_reason=tool_denied` |
| `S-EMPTY` | 2 consecutive empty/invalid tool args | End, `stop_reason=bad_args` |
| `S-LLM-ERROR` | API failure after retries exhausted | End, `stop_reason=llm_error` |

### 2.2 Skill-specific success stops

| Skill | Success condition | Notes |
|-------|-------------------|-------|
| `fill_ticket` | Successfully called `write_ai_output` and payload includes `customer_id`+`tag_id` (or ticket fields) | Story1 acceptance |
| `shared_write` | Successfully called `write_ai_output` | Asset write complete |
| `crm_lookup` | At least one master-data query done and model gives summary | Lookup loop closed |
| `channel_ops` | At least one health/alert query done and answer gives “number + anomaly + next step” | Dashboard loop closed |

Success stop implementation (does not conflict with max_steps):

1. Success is judged by `skill.success_when` in code.  
2. `max_steps` counts **only** tool rounds that include tools.  
3. On success, `break` out of the tool loop, then **start** one final answer call (`tools=None`).  
4. If not successful, run full max_steps → `max_steps`; no extra tool round.  
5. If final turn still returns tool_calls → `success_forced`.  

### 2.3 Business hard stops

See [Module 4](./04-module-4-security-limits-and-boundaries.md): outreach block, synthetic VIN, PII/secrets, Skill `security` slot, etc.

---

## 3. System Prompt structure

Concatenation order is **solely** determined by constant `PROMPT_SECTION_ORDER` (see `agents/react/skill_schema.py`); callers must not reorder:

```text
[A_base]          Enterprise identity + ReAct rules + anti-AI-silo rules
[B_tone]          Module 1 style labels and forbids
[C_goal]          This Skill one-line goal + success criteria
[C2_system_extra] Skill extra steps (skip if empty)
[D_tools]         Allowlist only; do not fabricate tool results
[E_output]        Final answer structure visible to user/agent (skip if empty)
[F_security]      Security boundary summary (Module 4; generated from skill.security)
```

`skill.yaml` field contract: [`skills/SCHEMA.md`](../../skills/SCHEMA.md). Security details: [Module 4](./04-module-4-security-limits-and-boundaries.md).

### 3.1 [A] Base (all Skills share)

See `agents/react/prompts.py` → `BASE_SYSTEM`:

- You are Qingshu Mobility’s internal ReAct Agent  
- Multiple departments share the same hands/feet; you represent **this Skill’s department role only**  
- Facts must come from tools; do not invent customer/vehicle/inventory/policy numbers  
- Cross-Skill collaboration via `write_ai_output` / `read_ai_outputs`; do not pretend to call other departments’ private stores  
- Synthetic data VINs start with `QS0`  

### 3.2 [B]+[C]+[E] per Skill (summary)

Full text lives in each `skills/*/skill.yaml` `system_extra`; table below for reference.

| Skill | Tone (Module 1) | Goal summary | Final answer structure |
|-------|-----------------|--------------|------------------------|
| `fill_ticket` | Calm confirm | Lookup master data → extract ticket fields → suggest tags → **write shared output** | Restate issue / draft fields / written output_id / next step |
| `crm_lookup` | Answer first | Look up customer·vehicle·order·inventory by ID and summarize | Conclusion within three lines + key fields |
| `channel_ops` | Ops dashboard | Lookup health/alerts/inspections, give actions | Numbers / anomalies / next step |
| `shared_write` | Neutral system | Assetize payload write | output_id + consumer_allow |

### 3.3 User message template

```text
【Skill】{skill_id}
【Input】{text or structured JSON}
【Known keys】customer_id=... vin=... (if any)
Complete the task within the tool allowlist; give final answer when success criteria are met.
```

---

## 4. DeepSeek call conventions

| Item | Value |
|------|-------|
| Base URL | `https://api.deepseek.com/v1` |
| Model | `deepseek-chat` (override with `DEEPSEEK_MODEL`) |
| Auth | `DEEPSEEK_API_KEY` |
| Tool calling | OpenAI compatible `tools` / `tool_calls` |
| Parse contract | `agents/react/tool_calls.py` (arguments as JSON string) |
| Temperature | Default `0.2` (ticket fill / data lookup should stay stable) |

Local config:

```bash
# .env (gitignored — do not commit)
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

---

## 5. Alignment with Story1

| Step | Expected |
|------|----------|
| 1 | `log_step` record start (optional) |
| 2 | `get_customer` / `get_vehicle` validate IDs |
| 3 | `extract_ticket_fields` + `suggest_voc_tags` |
| 4 | `write_ai_output` (producer=`fill_ticket`, consumer includes `renewal_plan`) |
| 5 | Calm-confirm final answer; `stop_reason=success\|final` |

---

## 6. Module 3 acceptance (self-check)

- [x] Unified ReAct workflow documented  
- [x] Global + Skill-specific stop conditions  
- [x] System Prompt section structure + per-Skill clauses  
- [x] DeepSeek client and `agents/react` control loop implemented  
- [x] CLI can run `fill_ticket` Story1  

---

## Revision history

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-02 | Module 3: workflow / stop conditions / Prompt + DeepSeek implementation |

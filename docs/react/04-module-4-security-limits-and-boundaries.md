# ReAct · Module 4: Security limits and boundaries

> **Core reference · Module 4** (depends on Modules 1–3)  
> Principle: **boundaries in code gates**; Prompt supplements only; shared tools ≠ open permissions  
> Version: V1.0 · 2026-08-02

---

## 1. Boundary overview (six layers)

```text
L1 Identity / synthetic data   VIN=QS0… · customer_id=CUS-… · no real brands in repo
L2 Tool permissions            Skill allowed_tools allowlist · producer_skill match
L3 Shared assets               PII/secrets forbidden · consumer_allow · block tags
L4 Department / Skill          kb domain dual gate · per-step tool cap · tone forbids
L5 Control loop                max_steps (tool rounds only) · +1 final turn after success · observation redaction
L6 Runtime secrets + scope     API keys in env; no production auth (see §7.2)
```

| Layer | Main enforcement | Failure / stop examples |
|-------|------------------|-------------------------|
| L1 | `shared/tools/guards.py` | `VIN_NOT_SYNTHETIC`, `INVALID_CUSTOMER_ID` |
| L2 | `ToolRegistry._assert_allowed` | `TOOL_NOT_ALLOWED`, `PRODUCER_MISMATCH` |
| L3 | `guard_payload` / `check_outreach_block` | `PII_FORBIDDEN`, `SECRET_FORBIDDEN` |
| L4 | `skill.yaml` → `security` + tool `kb_domains_allow` dual gate | `KB_DOMAIN_DENIED`, `TOO_MANY_TOOL_CALLS` |
| L5 | `agents/react/agent.py` | `max_steps`, `success` / `success_forced`, `security_stop` |
| L6 | `.env` + scope statement | No key → no LLM; do not claim enterprise ACL |

---

## 2. L1 · Identity and synthetic data

| Rule | Notes |
|------|-------|
| VIN | 17 chars, prefix `QS0` |
| customer_id | Prefix `CUS-` |
| KB domains | Only `repair/policy/hr/product/channel` |
| Brand narrative | Fictional Qingshu Mobility only; no real customer seeds |

If tools reject IDs, final answer must say “demo accepts synthetic IDs only”; do not invent real number ranges.

---

## 3. L2 · Tool permissions

| Rule | Notes |
|------|-------|
| Skill allowlist | `allowed_tools`; unlisted tool → `TOOL_NOT_ALLOWED` |
| No cross-Skill tool theft | e.g. `fill_ticket` must not call `score_renewal` (smoke locked) |
| Write impersonation | `write_ai_output.producer_skill` must equal `context.skill_id` |
| Unknown args | `additionalProperties=false` → `UNKNOWN_ARG` |
| Size | Text ≤4000 chars; payload ≤32KB; list limit ≤100 |

Cross-department: **read shared outputs/tags only**; no other dept business write tools.

---

## 4. L3 · Shared assets and outreach gate

| Rule | Notes |
|------|-------|
| No plaintext mobile | payload matches `1[3-9]xxxxxxxxx` → `PII_FORBIDDEN` |
| No secret shapes | payload contains `sk-…` / `API_KEY=` etc. → `SECRET_FORBIDDEN` |
| Consumer auth | `consumer_allow` controls `read_ai_outputs` |
| Outreach block | `TAG-open-complaint` / `TAG-reputation-risk` / `TAG-safety-hazard` → `allow_outreach=false` (Story2) |

ReAct renewal Skills with `security.block_on_outreach=true`: when `check_outreach_block.blocked=true`, loop **stops immediately**; no promo copy.

---

## 5. L4 · Department / Skill security slot (`security`)

See `skills/SCHEMA.md` and each `skill.yaml`:

| Field | Meaning |
|-------|---------|
| `kb_domains_allow` | When set, limits `search_kb` / `get_kb_document` / `list_kb_domains` (anti bypass) |
| `max_tool_calls_per_step` | Cap tool_calls per LLM turn |
| `redact_pii_in_observation` | Redact observation before model |
| `block_on_outreach` | Block tags → `security_stop` |
| `prompt_forbid_extra` | Hard forbid lines appended to Prompt |

### 5.1 Phase-1 Skill bindings

| Skill | Dept | Key boundary |
|-------|------|--------------|
| `fill_ticket` | Service | No over-promising compensation; no PII in writes; no renewal scoring tools |
| `crm_lookup` | Shared lookup | Read-only master data; no shared writes |
| `channel_ops` | Channel | Neutral tone; no personal attacks on dealers |
| `shared_write` | System | Neutral system voice; strong PII/secret gates |

---

## 6. L5 · Control loop hard gates

| Gate | Behavior |
|------|----------|
| `max_steps` | **Tool rounds with tools only** (`for step in 1..max_steps`) |
| Success +1 final turn | After success **exit tool loop**, one `tools=None` call; separate from max_steps count |
| Final turn still tool_call | → `success_forced` (success already; do not run tools) |
| Fail after max_steps | → `max_steps`; **no** extra tool round |
| Too many tools one step | → `security_stop` / `TOO_MANY_TOOL_CALLS` |
| KB domain bypass | Agent pre-check + `ToolContext.kb_domains_allow` dual gate on search/get/list kb |
| Observation redaction | Mobile → `1**********` before model |
| Repeated deny/bad args | `tool_denied` / `bad_args` |

---

## 7. L6 · Runtime secrets and “no production auth” scope

### 7.1 Runtime secrets (this demo does)

- `DEEPSEEK_API_KEY` only in `.env` / env (gitignored)  
- Prompts, logs, `AIOutput` must not echo full keys  

### 7.2 What “no production auth” means (scope statement, not a gap)

| Dimension | Demo **has** | Demo **explicitly does not** |
|-----------|--------------|------------------------------|
| Trust model | **Local trusted operator** runs CLI | Multi-tenant, anonymous public users |
| Permission model | **Skill tool allowlist** + synthetic ID checks + `consumer_allow` | SSO / OAuth / RBAC / row-level ACL |
| Identity | `skill_id` + `run_id` audit fields | Employee/store/dealer account systems |
| Audit | `log_step` / run logs (demo level) | Tamper-proof compliance audit, KMS |

**Wording:**

- OK: Skill-level tool isolation and shared-layer consumer auth (anti-AI-silo illustration)  
- Not OK: claim production enterprise auth / permission hub  

Productization auth is a **separate phase**, out of scope for this portfolio ReAct module.

---

## 8. Split with Prompt

| Mechanism | Owns |
|-----------|------|
| Code gates | Can call, can write, stop or not |
| Prompt (tone forbid + security appendix) | How to speak, what not to promise |
| Module 1 forbids | Fed to `tone.forbid`; does not replace code |

Append **`F_security`** to `PROMPT_SECTION_ORDER` (Module 4); `build_system_prompt` adds security summary.

---

## 9. Acceptance checklist

- [x] Six layers documented  
- [x] `skill.security` in schema and phase-1 Skills  
- [x] ReAct pre-check + observation redaction  
- [x] Payload blocks PII / secrets  
- [x] Story2 block tag rules preserved  
- [x] `scripts/smoke_react_security.py` covers key gates  

---

## Revision history

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-02 | Module 4 initial: six layers + code gates |

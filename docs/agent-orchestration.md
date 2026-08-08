# Agent orchestration: parallel vs sequential (read before wiring the web UI)

> Qingshu Mobility demo · Business wall `/business` + Ops desk `/ops`  
> **Architecture V2**: [BLUEPRINT.md](../BLUEPRINT.md) (platform 4 loops × 3 tool classes + Skills)  
> Machine-readable contract: `data/entities/department_flows.json`  
> Version: V1.2 · 2026-08-06

---

## 1. In one line

| Mode | Meaning | How the demo shows it |
|------|---------|------------------------|
| **Single-function run** | One Skill (one function) per run | Click one function card → one API run |
| **Parallel (relationship)** | Two functions with no hard data dependency; each can be try-run separately | Cards side by side; each has “open run” |
| **Sequential (relationship)** | Downstream usually needs upstream shared output; still **two independent runs** | Mark “depends on shared output”; **no** auto chain; **no** Agent handoff chat |

Anti-AI-silo rule: cross-function only via `AIOutput` / shared tags; **one function = one Skill**; no Multi-Agent chat or pipeline relay.

---

## 2. Priority decision table (for web UI)

### 2.1 Parallel (side-by-side try-run / display)

| Group | Members | Relationship note |
|-------|---------|-------------------|
| Story1 ticket dual path | Extraction `ticket_fields` ∥ ReAct `fill_ticket` | Same goal, optional paths; extract-before-fill not required |
| VoC dual Skills | `voc_entities` ∥ `voc_tagging` | Same schema alias; equivalent ops try-run |
| Repair RAG ⊥ Story1 | RAG `repair_kb` ⊥ ticket dual path | **Orthogonal parallel**: Q&A does not write ticket main path; fill does not depend on RAG |
| App RAG ⊥ renewal gate | RAG `F-UO-009` ⊥ Story2 gate | Renewal does not read RAG answers |
| Policy RAG ⊥ order review | RAG `policy_kb` ⊥ `order_policy_review` | Policy Q&A does not replace Rule tier gate |
| Channel board prep | ReAct `channel_ops` ∥ RAG `policy_kb` | Parallel fetch metrics / policy copy; **merge Planning still planned** |
| Quality prep | Vision ∥ Extraction | Parallel evidence then sequential merge (illustrative) |
| HR RAG | `hr_rules` single node | Standalone; cross-department read same domain only |

### 2.2 Sequential (upstream first, then downstream note)

| Chain | Order | Web UI behavior |
|-------|-------|-----------------|
| Story2 renewal gate | Upstream Extraction/ReAct writes block tag → shared layer → downstream renewal outreach | `F-UO-017` etc. marked “sequential downstream”; step copy, no chained run |
| Order review | Extraction extract → Rule+LLM gate → ReAct lookup | Order dept “display” + sequential note |
| Channel board merge | (after parallel prep) → Planning merge | Merge node planned |
| Quality merge | Vision∥Extraction → Rule alert | IoT display |

**RAG’s own control loop is linear** (retrieve → stuff → generate → cite), but relative to other loops it **does not create cross-loop sequential dependency** (except channel board “merge” illustration).

### 2.3 RAG machine-readable flows (`department_flows.json`)

| flow_id | Skill | With other loops |
|---------|-------|------------------|
| `service_repair_qa` | `repair_kb` | ∥ Story1 |
| `user_ops_app_qa` | `repair_kb` | ∥ renewal gate |
| `order_policy_qa` | `policy_kb` | ∥ order review illustration |
| `hr_policy_qa` | `hr_rules` | standalone |
| `channel_ops_board` | `channel_ops` ∥ `policy_kb` → Planning | Parallel prep; merge planned |

---

## 3. Phase-1 runnable paths (summary)

### 3.1 Parallel (same story, different loops)

```text
Same business goal “ticket draft assetization / Story1”:

  [Extraction · ticket_fields]  ──┐
                                  ├──► write_ai_output ──► shared layer
  [ReAct · fill_ticket]         ──┘

Also: [RAG · repair_kb]  ──► cited final answer (orthogonal to above; not on write-shared main path)
```

### 3.2 Sequential (requires upstream tags)

```text
Story2 renewal gate:

  Upstream (service/VoC Extraction or ReAct fill)
        │  write_ai_output (with block tag)
        ▼
  Shared layer Tag / AIOutput
        │  read_shared_tags / check_outreach_block
        ▼
  Downstream Planning/Rule (renewal outreach) — phase-1 contract exists; loop may still be planned
```

Web copy guidance:

1. First run **demo-ready** Extraction or ReAct fill on service/user-ops to write complaint/risk tags.  
2. Then open user-ops “complaint gate” card (display + sequential dependency note); full `renewal_plan` run belongs to Planning track.

---

## 4. Web wiring rules (this step)

| Page | Demo-ready (`demo_ready`) | Not in demo |
|------|---------------------------|-------------|
| **Business wall `/business`** | One card = one Skill calling matching API; show shared dependency notes | Planned cards display-only |
| **Ops desk `/ops`** | **Troubleshooting**: log stream / metrics / traces / shared outputs | **No** Skill try-run or policy Q&A |

API mapping:

| Loop | Endpoint |
|------|----------|
| ReAct | `POST /v1/react/runs` |
| Extraction | `POST /v1/extraction/runs` |
| RAG | `POST /v1/rag/runs` |

Do not: one-click auto chain across multiple loops (avoids phase-1 scope blow-up).

---

## 5. Revisions

| Version | Notes |
|---------|-------|
| V1.2 | Ops desk corrected to troubleshooting (not Skill try-run wall) |
| V1.1 | RAG decision table; dual-page demo includes RAG; channel parallel prep note |

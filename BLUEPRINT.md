# Qingshu Mobility · Anti-AI-Silo Platform Blueprint (V2)

> **Purpose**: Portfolio reference implementation (digital transformation consulting)  
> **Scope**: Runnable demo — not a client delivery, not a production platform  
> **Brand**: Fictional smart EV mobility company **Qingshu Mobility**  
> **Version**: V2.1 · 2026-08-07 — **one business function = one Skill**; cross-function work only via the shared layer; no Agent-to-Agent chat or pipeline handoff  

Related docs: [Design decisions](./docs/design-decisions.md) · [Consulting narrative](./docs/consulting-narrative.md) · [What the platform owns](./docs/shared-vs-not-shared.md) · [Planning](./docs/planning/01-module-1-background-and-orchestration.md)

---

## 0. One-line product definition

A governable enterprise AI product is:

**Platform-managed Control Loops + Tools**, plus department-built **Skills**.

Anti-AI-silo is not “share one Agent / a few persona Agents” (teams still rebuild loops and tools). It is:

| Platform release & governance | Department delivery |
|-------------------------------|---------------------|
| A limited set of **control loops** (cognitive execution modes) | Department **Skills** (goal, tone, allowlist, schema/index slots) |
| A unified **tool ledger** (by governance class) | Use approved tools only; no private DataFetcher |
| Shared semantics / `AIOutput` / capability catalog | Read/write shared outputs; no direct access to other teams’ private stores |

### 0.1 One function = one Skill (runtime rule)

| Do | Don’t |
|----|-------|
| **Each business function = one Skill**; one run picks one `skill_id` | Hand off from one Agent chat to the next |
| Finish the job inside **this Skill’s tool allowlist** | Treat “Extract loop then Act loop” as the default product path |
| To reuse prior results: start another run and **read the shared layer** | Multi-Agent chat / auto-pipeline of many Skills |

`department_flows` only describes optional shared-output dependencies or parallel relations for docs and governance. It is not a runtime Agent relay orchestrator.

This architecture is also not: one company-wide “super brain” / System Prompt; per-department isolated Agent stacks; a single enterprise Orchestrator for all teams; Agent-to-Agent chat as cross-function collaboration.

---

## 1. Platform axes

| Axis | Content |
|------|---------|
| **Platform Control Loops (4)** | Retrieve · Act · Extract · Plan |
| **Platform Tools (3 classes)** | Read · Knowledge · Write/Govern |
| **Department Skills (N)** | **One function = one Skill**; bound to one loop; one Skill per run |
| **Relation contract** | `department_flows`: dependency / parallel notes via shared outputs (not an Agent pipeline) |

Rule+LLM and Vision are explained as Plan (gate sub-mode) and Extract (perception / structure sub-mode). Code folders may stay as extensions; they are not on the platform main list.

---

## 2. Logical layers (platform view)

```text
┌─────────────────────────────────────────────────────────────┐
│ L1 Entry (minimal)                                          │
│  CLI / FastAPI: control_loop + skill_id + input             │
│  Business wall `/business`: Skills by department (try-run)  │
│  Ops desk `/ops`: troubleshooting (logs / metrics / traces) │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ L2 Platform control loops (4) · release & governance        │
│  Retrieve(RAG) | Act(ReAct) | Extract | Plan(Planning)      │
│  One implementation per loop; no per-department copies      │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ L3 Skill layer · department deliverable                     │
│  Goal / tone / tool allowlist / schema·index·decision slots │
│  e.g. repair_kb · fill_ticket · ticket_fields · renewal_plan│
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ L4 Relation notes & collaboration (demo-light)              │
│  Each run: one skill_id; run_id + step logs                 │
│  flows: shared dependency notes; cross-function via AIOutput│
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ L5 Platform tools (3-class ledger)                          │
│  Read | Knowledge | Write/Govern — single ToolRegistry      │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ L6 Unified DataFetcher                                      │
│  Fake CRM / tickets / KB / orders… one place; loops call it │
└────────────────────────────┬────────────────────────────────┘
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ L7 Shared asset layer (explicit anti-silo layer)            │
│  Unified models · tag vocab · AIOutput · CapabilityCatalog  │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Architecture principles

| Principle | Meaning |
|-----------|---------|
| Product trio | **Loops + Tools + Skills** |
| Platform owns loops & tools | Unified release, allowlists, audit language |
| Departments ship Skills only | No copied loops, DataFetchers, or private tool impls |
| Anti-silo at L7 + Write/Govern | Shared semantics, subscribable outputs, searchable capabilities |
| One function = one Skill | One function per run; no Agent→Agent chat relay |
| Relations via shared layer | flows document deps; consumers start a new run to read `AIOutput`/tags |
| No single Orchestrator | Many loops coexist; entry is always `control_loop + skill_id` |

---

## 3. Four platform control loops

| Loop ID | Directory | Loop shape | Demo Skills (examples) | Status |
|---------|-----------|------------|------------------------|--------|
| **retrieve** | `agents/rag/` | retrieve → stuff → generate → cite | `repair_kb` · `policy_kb` · `hr_rules` | Ready |
| **act** | `agents/react/` | think → act → observe | `fill_ticket` · `crm_lookup` · `channel_ops` | Ready |
| **extract** | `agents/extraction/` | schema → extract → validate | `ticket_fields` · `voc_entities` · `voc_tagging` | Ready |
| **plan** | `agents/planning/` | read shared → gate / multi-step plan → (optional) downstream | `renewal_plan` (Story2) | Ready |

**Sub-modes (not separate platform loops):**

- **Rule gate** → under Plan (or hard-stop tools in Act, e.g. `check_outreach_block`)  
- **Vision** → under Extract perception input, or a later split  

API / CLI primary IDs are `retrieve` / `act` / `extract` / `plan`. Legacy names `rag` / `react` / `extraction` / `planning` stay via alias tables (`apps/loops.py`, `data/entities/control_loop_aliases.json`). Skill YAML and existing `/v1/{rag|react|extraction}/runs` paths still use legacy names for now.

---

## 4. Three tool classes (governance ledger)

Implemented under `shared/tools/`. Governance view uses three classes:

| Class | Meaning | Examples in repo |
|-------|---------|------------------|
| **read** | Master / transaction / ops read-only | `get_customer` · `get_ticket` · `list_renewals` · channel/order reads… |
| **knowledge** | Knowledge retrieval | `search_kb` and related |
| **write_govern** | Shared write, tagging, outreach gate, catalog | `write_ai_output` · `read_ai_outputs` · `check_outreach_block` · `list_capabilities` · `log_step` |

Rules:

- All loops call tools only via ToolRegistry; no private fetcher/tool copies  
- Skills declare a subset with `allowed_tools` (or the capability catalog)  
- Business-domain labels (service/channel…) may be secondary indexes; the main axis is the three classes  
- Runtime map: `shared/tools/governance.py` · machine ledger: `data/entities/tool_class_map.json` · API: `GET /v1/tools?tool_class=`

---

## 5. Skills and relation contracts

### 5.1 Skill

- Belongs to one platform loop (`control_loop` + `apps/skill_loops.py`)  
- Carries department tone, success criteria, tool allowlist, schema/index slots  
- Machine-readable relations live mainly in `data/entities/department_flows.json` (nodes = independently runnable Skills); `skill.yaml` may reference `# flow:`  

### 5.2 Flows (relation notes, not a run engine)

See `docs/planning/`:

- Each node is one independently runnable Skill (or a placeholder)  
- `mode: sequence` — data dependency: the downstream Skill usually needs upstream writes in the shared layer (still two separate runs)  
- `mode: parallel` — either Skill may be demoed alone; no forced order  
- Cross-department edges only via L7  

Demo acceptance (two independent Skill runs, store in between):

| Story | Meaning |
|-------|---------|
| **Story1** | Run `fill_ticket` or `ticket_fields` → `write_ai_output` |
| **Story2** | Separately run `renewal_plan` (Plan) → read shared tags → block outreach |

Without Story2, do not claim “anti-AI-silo is demonstrated.”

---

## 6. Repository layout

```text
enterprise-anti-ai-silo-demo/
├── BLUEPRINT.md                 # this file (V2 platform architecture)
├── README.md
├── docs/
│   ├── design-decisions.md
│   ├── consulting-narrative.md
│   ├── shared-vs-not-shared.md
│   ├── planning/
│   ├── react|extraction|rag/
│   └── agent-orchestration.md
├── shared/                      # platform infra L5–L7
│   ├── models/ · store/ · datafetcher/ · tools/
├── agents/                      # control loops only
│   ├── rag/ · react/ · extraction/ · planning/
│   ├── rule_llm/ · vision/      # extensions (not main platform list)
├── skills/
├── data/entities/department_flows.json
└── apps/                        # CLI + API
```

---

## 7. Explicit non-goals

- Multi-Agent chat orchestration  
- Real CRM / ERP / SSO / message queues / production auth and distributed locks  
- Model fine-tuning or complex cockpits presented as a “live platform”  
- Real customer data and brands  
- Replacing the four loops with one Orchestrator  
- Promoting Rule+LLM / Vision to peer platform loops  

---

## 8. Tech choices (summary)

| Item | Choice |
|------|--------|
| Language | Python 3.11+ |
| LLM | OpenAI-compatible (e.g. DeepSeek); keys in env vars |
| Models | Pydantic; Skill YAML |
| Entry | CLI + FastAPI |
| Collaboration | run_id + `shared/store` |
| Evaluation | Extraction / RAG gold sets; Story1/2 smoke tests |

---

## 9. Positioning note

This repo is a Qingshu Mobility anti-AI-silo reference: platform governance of **4 control loops + 3 tool classes**, with business **Skills**; shared semantics, AI output assets, and Story1/2.  
It is not a live enterprise AI platform and not a multi-department production delivery.

---

## 10. Completeness checklist

- [x] Product defined as Loops + Tools + Skills  
- [x] Platform 4 loops + 3 tool classes  
- [x] Departments ship Skills only  
- [x] Unified ToolRegistry + DataFetcher  
- [x] Explicit shared asset layer  
- [x] One function = one Skill; cross-function only via shared layer  
- [x] flows are relation notes, not a run engine  
- [x] Story1 / Story2 acceptance (two independent runs)  
- [x] Non-goals and positioning note  
- [x] Fictional brand: Qingshu Mobility  

This document is the current architecture (V2).

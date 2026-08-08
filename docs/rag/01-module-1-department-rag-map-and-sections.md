# RAG · Module 1: Department × RAG section map

> **Core reference · RAG Module 1** (blueprint `agents/rag/`)  
> Fictional company: **Qingshu Mobility** · smart EV mobility  
> Control loop: `retrieve → stuff → generate`  
> Principle: **one RAG loop**; dept/function variance in **Skill + kb_domain**; no per-dept index engine copies  
> Version: V1.0 · 2026-08-05

---

## 0. Scope

| Concept | Meaning |
|---------|---------|
| **RAG loop** | Standalone loop: retrieve → context stuff → generate; ops `agent_type=rag` |
| **Skill** | Domain mount, prompt slots, success criteria (e.g. `repair_kb` / `policy_kb` / `hr_rules`) |
| **kb_domain** | Knowledge partition: `repair` · `policy` · `hr` · `product` · `channel` (see `data/knowledge/`) |
| **ReAct + search_kb** | Tool path can query KB — **not** the RAG loop itself; orthogonal, can parallel |

This doc lists **all departments** with “RAG-primary” functions and marks phase-1 demo vs spec placeholder.  
Relationships: [02](./02-module-2-cross-agent-relationship-orchestration.md); phase-1 cut: [03](./03-module-3-phase-1-demo-scope-and-schedule.md).

---

## 1. Knowledge domain ↔ Skill (base)

| kb_domain | Sample docs | Suggested Skill | Primary consumers |
|-----------|-------------|-----------------|-------------------|
| `repair` | Range/motor/binding/brake/charging | `repair_kb` ★ | Service · User ops/App · IoT |
| `policy` | Warranty/battery · pickup rebate · renewal red lines · store VI | `policy_kb` ★ | Order/policy · Channel · War zones · User ops |
| `hr` | Employee policy · agent SOP | `hr_rules` ★ | HR · (agent QC side path) |
| `product` | Model selling points · OTA notes | `product_kb` | New retail · Product ops · App |
| `channel` | Pickup talk track · store opening checklist | `channel_kb` | Channel ops · War zones |

★ = blueprint phase-1 mounted Skills; `product_kb` / `channel_kb` reuse same RAG loop; YAML phased in.

Cross-dept base: `F-X-001` digital asset library, `F-DAT-010/011/012` — **supply layer**, not a second retrieval engine.

---

## 2. Catalog department × RAG sections

Aligns with `apps/catalog.DEPARTMENTS`. Columns:

- **RAG section**: in-dept blocks where RAG is primary (or heavy KB Q&A)  
- **Feature ID**: from `docs/ai-feature-requirements.md`  
- **Demo**: ✅ phase-1 must · 📋 spec placeholder · — no standalone RAG primary (shared consume / side path only)

### 2.1 Service `service`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| Smart assist reply | F-SVC-002 | `repair_kb` · repair | ✅ | Agent desk script/KB recommend main path |
| Repair KB Q&A | F-SVC-004 · F-DAT-011 | `repair_kb` | ✅ | Same Skill as F-SVC-002, different entry copy |
| Repair service desk | F-SVC-003 | repair + ReAct vehicle/ticket | 📋→side | **Q&A primary RAG**; master-data steps via ReAct (parallel prep) |

### 2.2 User ops / App `user_ops`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| App smart Q&A MVP | F-UO-009 | `repair_kb` (+ some product) | ✅ | Reduce hotline; shared domain with service; optional `app_qa` alias |
| KB auto-update | F-UO-010 | Extract → write kb | 📋 | RAG **consumes** updated library; update pipeline not RAG loop |
| AIGC copy/Push | F-UO-013 | product/policy retrieval boost | 📋 | Retrieval as material; generation may be Plan |
| Unified smart service | F-UO-019 | repair + ReAct | 📋 | Phase 2; Q&A reuses `repair_kb` |

### 2.3 Order / policy `order_policy`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| Policy copy Q&A | F-OPS-004 side | `policy_kb` · policy | ✅ | Parse primary Extract+Rule; **pure Q&A** via RAG |
| Franchise risk KB assist | F-OPS-006 | policy + risk text | 📋 | Rule gate primary; RAG for clause retrieval |

### 2.4 War zones `warzone`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| Offline Q&A RAG | F-WZ-001 | policy/channel/product | 📋 | Dealer/store Q&A; phase-1 card display, run via `policy_kb` |
| Pickup plan talk track | F-WZ-001 sub | channel | 📋 | Same domain as channel `channel_kb` |

### 2.5 Channel ops `channel`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| Channel/policy KB Q&A | F-OPS-001 KB segment | `channel_kb` / `policy_kb` | ✅ illustrative | **Parallel** with ReAct `channel_ops` (flow `channel_ops_board`) |
| Store opening KB | F-OPS-013 side | channel | 📋 | Plan produces pack; RAG answers “opening checklist how-to” |

### 2.6 New retail `retail`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| Multi-platform service KB | F-RET-001/002 | product (+repair) | 📋 | ReAct order/inventory; KB segment parallel RAG |

### 2.7 Procurement `procurement`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| Partnership risk clause retrieval | F-PUR-002 | dedicated domain (none) | 📋 | No procurement kb phase 1; card display |

### 2.8 Data lab / digital assets `data_lab` · `shared`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| Internal KB base | F-DAT-010 · F-X-001 | all-domain index | ✅ base | **Index/chunk/domain routing** in shared layer, not a business Skill |
| Metric semantic Q&A | F-DAT-002 | semantic dictionary | 📋 | Ask-data primary ReAct/Text2SQL; RAG gloss side path |
| Asset structured ingest | F-DAT-012 | Extract → kb | 📋 | Supply pipeline |

### 2.9 HR platform `hr`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| Policy Q&A / employee assistant | F-HR-001 · F-HR-003 | `hr_rules` · hr | ✅ | Phase-1 Skill; cross-dept read-only same library |
| Recruiting service KB | F-HR-002 | hr | 📋 | Match segment Extract; Q&A segment RAG |

### 2.10 IoT / vehicle `iot`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| OTA/fault KB side path | F-IOT-002 side | product/repair | 📋 | Primary Rule+LLM; RAG explains version docs |

### 2.11 VoC / research `voc`

| RAG section | Feature ID | Skill / domain | Demo | Notes |
|-------------|------------|----------------|------|-------|
| VoC Agent scenario guide | F-VOC-022 | methodology/playbook kb | 📋 | Plan+RAG; no VoC playbook library phase 1 |

---

## 3. Outside catalog (full requirements; demo display/placeholder only)

| Dept (requirements list) | RAG section examples | Feature ID | Demo |
|--------------------------|------------------------|------------|------|
| Strategy / management | Ask-data gloss, social/competitor quarterly | F-STR-001/005 | 📋 |
| Brand ops / institute | GEO, MI text, social image, asset copy | F-BRD-007/008/014 etc. | 📋 |
| Product ops / tech institute | Competitor intel, R&D insight, motor/battery graph | F-PRD-001/002/004/005 | 📋 |
| Legal compliance | Contract clause retrieval | F-LEG-001 | 📋 |
| Executive office | Press release material retrieval boost | F-SEC-001 | 📋 |
| IT / process | Organizational memory vector store | F-IT-005 | 📋 |
| Manufacturing / quality | (Vision primary; no standalone phase-1 RAG) | — | — |
| Supply / finance / retail QC | Occasional clause retrieval, no dedicated Skill | — | — |

---

## 4. Overview: phase-1 must-run RAG assets

| Priority | skill_id | kb_domains_allow | Features | Status (at doc time) |
|----------|----------|------------------|----------|-------------------|
| P0 | `repair_kb` | `repair` | F-SVC-002/004 · F-UO-009 · F-DAT-011 | Catalog placeholder; loop later built |
| P0 | `policy_kb` | `policy` | Policy Q&A · channel parallel · F-OPS side | Catalog placeholder |
| P0 | `hr_rules` | `hr` | F-HR-001/003 | Directory+YAML to build |
| P1 | `channel_kb` or reuse policy | `channel` | `channel_ops_board` RAG node | planned |
| P2 | `product_kb` | `product` | New retail/App selling Q&A | planned |

Machine-readable catalog has `repair_kb` / `policy_kb` entries (`capability_catalog.json`); **missing** loop + `skill.yaml` at doc time.

---

## 5. Related docs

| Doc | Relation |
|-----|----------|
| [02 · Relationships](./02-module-2-cross-agent-relationship-orchestration.md) | Parallel/sequential/orthogonal |
| [03 · Phase-1 scope](./03-module-3-phase-1-demo-scope-and-schedule.md) | In/out/schedule |
| [docs/planning/02](../planning/02-module-2-department-flow-diagrams.md) | Channel flow includes RAG parallel node |
| [docs/react/02](../react/02-module-2-department-toolbox.md) | ReAct `search_kb` allowlist |
| [BLUEPRINT.md](../../BLUEPRINT.md) | L2 RAG · L3 Skill · D7 schedule |

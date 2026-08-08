# ReAct · Module 1: Background, cross-department features, tone

> **Core reference · Module 1** (blueprint `agents/react/`)  
> Fictional company: **Qingshu Mobility** · smart EV mobility  
> Principle: departments share **one ReAct control loop + Tool/DataFetcher**; variance lives in **Skills (function goal + tone)**  
> Version: V1.0 · 2026-08-02

---

## 1. Background

### 1.1 Company and demo scope

Qingshu Mobility is a fictional smart EV mobility company. Departments used to build separate Agents and duplicate data access → **AI silos ≈ data silos**.

This demo’s ReAct is not “one brain per department”:

| Axis | Approach |
|------|----------|
| Technical type | Single **think → act → observe** control loop |
| Business variance | Multiple **Skills** (ticket fill, master-data lookup, channel ops, shared write…) |
| Anti-AI-silo | Shared Tool / DataFetcher / tag dictionary / `AIOutput` |

### 1.2 Why ReAct here

ReAct fits **multi-step tool calls with observation closure**, e.g.: lookup customer → vehicle → open tickets → draft ticket → `write_ai_output`.

Not ReAct-only (other loops handle these):

| Type | Typical capability |
|------|-------------------|
| RAG | Pure knowledge Q&A (repair/policy/HR long docs) |
| Plan | Multi-day renewal campaigns, weekly brief orchestration |
| Extract | Pure structured field extraction |
| Rule+LLM | Hard rule gates (renewal routing, policy tiers) |
| Vision | Inspection / QC images |

### 1.3 Module 1 outputs

Defines **who (department) needs what capability and tone** for later modules:

| Later module | Uses from this module |
|--------------|----------------------|
| Module 2 · Toolbox | Attach tools per features below |
| Module 3 · Workflow / System Prompt | Write “function goal + tone” into Skill prompt slots |
| Module 4 · Security | Hard limits on sensitive dept copy |
| Module 5 · UI / API | Show Skills per department entry |

---

## 2. Cross-department feature list (ReAct axis)

> Scope: capabilities needing **tool lookup / multi-step closure** only; pure RAG/Vision etc. excluded.  
> Feature IDs align with `docs/ai-feature-requirements.md`.

### 2.1 By department

| Department | Feature | One-line purpose | Feature ID | Phase-1 demo |
|------------|---------|------------------|------------|--------------|
| **Service** | Smart ticket fill | Dialog → ticket draft → shared output | F-SVC-001 | ✅ `fill_ticket` (Story1) |
| **Service** | Repair assist multi-step | Lookup vehicle/ticket/knowledge → actionable answer | F-SVC-003 | ✅ can use `crm_lookup` + `search_kb` |
| **User ops / App** | Renewal AI outbound | Lookup renewal pool + intent → outreach copy | F-UO-001 | △ Planning may own; lookup segment uses ReAct |
| **User ops / App** | Agent proactive outreach | Read telemetry / complaint tags → decide outreach | F-UO-017 | ✅ Story2 tag consumer |
| **User ops / App** | Unified smart service | App multi-step master-data then answer | F-UO-019 | △ phase-2 feel; phase-1 illustrative |
| **Ops · order/policy** | Smart order review | Inventory→policy→substitute→status suggestion | F-OPS-003 / F-X-004 | △ illustrative Skill, not Story must-run |
| **Four war zones** | Pickup/order assist | Store-side inventory+policy action list | F-WZ-001 / 002 | △ shares tools with order review |
| **Channel ops** | Health/alert lookup | Health index, alerts, inspection slice | F-OPS-012 related | ✅ `channel_ops` |
| **New retail** | Multi-platform auto-reply | Orders/inventory/campaigns then reply | F-RET-001 / 002 | △ illustrative |
| **Procurement** | PO follow-up / expedite | PO→logistics→overdue reminder | F-PUR-001 / 003 / 004 | △ illustrative |
| **Data lab** | Smart ask-data | Clarify metric→semantic layer→numbers | F-DAT-003 / F-X-002 | △ illustrative (may simplify to table tools) |
| **HR platform** | Employee AI assistant | Policy Q&A then optional process step lookup | F-HR-001 | △ Q&A mainly RAG; process steps may use ReAct |
| **IoT / vehicle** | Telemetry proactive service | Alerts/mileage → suggested action → write output | F-IOT-003 | △ illustrative |

### 2.2 Cross-department shared capabilities

| Capability | Departments | Purpose | Skill / Tool |
|------------|-------------|---------|--------------|
| Master-data composite lookup | Service / ops / war zones / user ops | Same customer·vehicle·order·ticket IDs | `crm_lookup` |
| Shared output write | All (service first) | Assetize output for other Skills | `write_ai_output` / `shared_write` |
| Shared tag/output read | User ops / channel / management | Cross-Skill consume, block bad outreach | `read_ai_outputs` / `read_shared_tags` |
| Capability catalog search | All | Discover existing Skills, avoid duplicate Agents | `list_capabilities` |
| Channel ops lookup | Channel / war zones / retail QC consumers | Same data source for ops and compliance | `channel_ops` |

### 2.3 Phase-1 must-run mapping

| Story | Skill | Dept narrative | Anti-AI-silo point |
|-------|-------|----------------|-------------------|
| Story 1 | `fill_ticket` | Service ticket fill | Writes `AIOutput` |
| Story 2 | `renewal_plan` (Planning) reads service output | User ops renewal | Open complaint tag → **block outreach** |

---

## 3. Tone and style (by department)

> Style lives in **Skill prompt slots**, not ReAct loop code.  
> Short labels for Module 3 reference.

| Department | Style label | Tone (≤3 bullets) | Forbidden |
|------------|-------------|-------------------|-----------|
| **Service** | **Calm confirm** | Restate issue; short fact checks; actionable next step | Over-promising “will fix/compensate for sure” |
| **User ops / App** | **Nudge not push** | Clear benefit; one question at a time; de-escalate when sensitive | Scare tactics; push renewal ignoring complaints |
| **Ops · order/policy** | **Policy precise** | Action first; cite policy basis; mark “needs human” if unsure | Fabricated rebate numbers |
| **Four war zones** | **Frontline direct** | Conclusion first; numbered actions; few adjectives | Long comfort talk, empty motivation |
| **Channel ops** | **Ops dashboard** | Numbers + anomaly + next step; neutral tone | Personal attacks on dealers |
| **New retail** | **Shelf guide** | Conversion-focused; substitutes or store path if OOS | Fake inventory, fake promo price |
| **Procurement** | **Milestone track** | Clear timestamps; polite firm follow-up | Blame suppliers or internal teams |
| **Data lab** | **Answer first** | Number first; then definition and limits; say if no data | Invent metrics |
| **HR platform** | **Friendly neutral** | Policy text first; sensitive topics → HRBP | Fabricated benefits/pay rules |
| **IoT / vehicle** | **Alert brief** | Severity → symptom → action; three lines max | Scare user; excessive jargon |
| **System/shared** (read/write output) | **Neutral system** | Describe asset/state only, not a business persona | Service comfort voice, tele-sales voice |

### 3.1 Skill ↔ style (phase 1)

| Skill | Owner dept | Style label |
|-------|------------|-------------|
| `fill_ticket` | Service | Calm confirm |
| `crm_lookup` | Multi-dept shared | Answer first (minimal small talk) |
| `channel_ops` | Channel ops | Ops dashboard |
| `shared_write` / read shared tags | All | Neutral system |

---

## 4. Module 1 acceptance (self-check)

- [x] Qingshu background and “shared ReAct, Skills carry dept variance”  
- [x] ReAct-oriented features by department with phase-1 / illustrative tags  
- [x] Cross-dept shared capabilities and Story1/2 mapping  
- [x] Each department: style label + tone bullets + forbidden list  
- [x] Phase-1 Skills bound to styles for Module 2 toolbox  

---

## Revision history

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-02 | Module 1 complete: background + cross-dept features + tone |

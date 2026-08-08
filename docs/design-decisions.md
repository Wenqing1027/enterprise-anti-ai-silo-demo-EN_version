# Design decisions (Qingshu Mobility · Anti-AI-Silo)

> **Status**: Architecture-level ADR set; companion to [BLUEPRINT.md](../BLUEPRINT.md).  
> **Version**: V2.1 · 2026-08-07  
> **Scope**: Principles and trade-offs only; no UI interaction specs.

---

## DD-01 · Product definition: Loops + Tools + Skills

**Decision**: A governable enterprise AI product splits into three parts — platform control loops, platform tools, department Skills.

**Rationale**: Calling delivery “we deployed a few Agents” is not auditable (persona/Prompt/private scripts mixed). The three parts map to: cognitive execution modes, approved side-effect boundaries, business variance config.

**Consequence**: Demo narrative and docs center platform governance; “department Agent” is no longer a first-class architecture citizen.

---

## DD-02 · Anti-AI-silo via platform loops and tools, not shared Agents

**Decision**: Preventing AI silos = unified release/allowlist/shared assets; **not** “one company-wide Agent (or a few).”

**Rationale**: Shared Agents still lead departments to copy Prompts, data access, and half-loops. Duplication is in loops and tools, not in whether Agent names are shared.

**Consequence**: Business view browses **Skills** by department and try-runs; **ops view** sees runtime (logs / metrics / traces / shared output health), **not** another “regulations-by-loop / RAG try-run” business wall.

---

## DD-03 · Platform control loops converge to 4 (Retrieve / Act / Extract / Plan)

**Decision**: Platform main list keeps four loops; legacy six-type Rule+LLM and Vision become sub-modes or extension slots.

| Loop | Solves | Does not solve |
|------|--------|----------------|
| Retrieve | Long-doc Q&A with citations | Multi-step writes, hard gates |
| Act | Multi-step tool closure | Pure schema extraction, campaign orchestration |
| Extract | Structured extraction and validation | Open-domain chat, complex planning |
| Plan | Gates / multi-step plans after reading shared layer | Replacing ToolRegistry |

**Rationale**: Four loops cover the consulting story and shipped demo capabilities; a six-type list dilutes “what the platform owns.”

**Consequence**: `agents/rule_llm/`, `agents/vision/` may remain as extensions, **not** on the platform main acceptance list. Plan loop is required for the platform narrative (Story2).

---

## DD-04 · Tool governance axis: 3 classes (Read / Knowledge / Write-Govern)

**Decision**: Platform tool ledger primary taxonomy is three classes; business domain (service/channel…) is secondary.

**Rationale**: Governance must answer “who reads master data / searches knowledge / writes shared layer and outreach.” Domain tags help dev search but are not the governance language.

**Consequence**: Catalog/docs show three classes first; handlers need not live in separate dirs — use `category` or mapping.

---

## DD-05 · Business variance only in Skills; no copying loops or DataFetcher

**Decision**: Department differences (goal, tone, allowlist, schema/index) live only in `skills/`; loop dirs must not host private `data_fetcher` or private tool impls.

**Rationale**: Dedup and governance are the same line: loop/tool changes once, all Skills benefit.

**Consequence**: New department = new Skill (or YAML edit), not a new Agent project.

---

## DD-06 · Cross-function only via shared outputs; no Agent chat or pipeline relay

**Decision**: If function A relates to B, only via `AIOutput` / tags / schema; **two independent runs**. No Agent chat bus, no “upstream loop auto-hands to downstream.”

**Rationale**: Chat/pipeline is slow and hard to govern; shared assets are auditable and blockable (Story2).

**Consequence**: `department_flows` is a **relationship spec** (who wrote what, who may read), not a chained-run engine. Planning docs describe Plan **Skills** and dependency notes, not Agent chat orchestration.

---

## DD-07 · No enterprise single Orchestrator

**Decision**: Multiple loops coexist; forbid one central orchestrator for all departments/Skills.

**Rationale**: Single Orchestrator slides toward “mega brain,” conflicts with consulting anti-patterns, and is too heavy to build.

**Consequence**: Entry is always `control_loop + skill_id`; phase 1 does not auto chain multiple Skills.

---

## DD-13 · Two pages: business try-run ≠ ops troubleshooting

**Decision**:

| Page | Audience | Does | Does not |
|------|----------|------|----------|
| `/business` | Business departments | One card = one function = one Skill try-run | Act as monitoring console |
| `/ops` | Tech ops / SRE | Troubleshooting: health / golden metrics / event correlation / root cause / **four-loop subpages** / call chain | Regulations Q&A or second Skill wall |

**Rationale (correction)**: Early ops desk was “try-run Skills by agent_type,” so ops became a business capability desk (especially Retrieve like policy Q&A), misaligned with IT troubleshooting.

**Consequence**: Skill try-run stays on business wall (and CLI/API); ops consumes `run_logs` / `ai_outputs` / health metrics; `/ops/embed` is troubleshooting panel, not RAG try-runner.

---

## DD-12 · One function = one Skill (runtime)

**Decision**: Each business function maps to one Skill; user/API runs one `skill_id` to completion. Multi-step tool use stays inside **that Skill + that loop** (e.g. Act think→act→observe).

**Rationale**: Matches “no passing results to the next Agent”; deliverables are countable, authorizable, evaluable.

**Consequence**:

- **No need** to rewrite existing Skill YAML for “no Agent relay” (`fill_ticket`, `ticket_fields`, `repair_kb` are already full functions).  
- `ticket_fields` and `fill_ticket` are **two optional functions** (extract-only vs multi-step fill), not a required Agent pipeline.  
- Story2 = run `renewal_plan` reading shared layer, not Plan Agent chatting with service Agent.

---

## DD-08 · Collaboration layer demo-light

**Decision**: `run_id` + step logs + local store; no distributed locks, message queues, or real SSO.

**Rationale**: Portfolio proves “shared outputs consumable across loops”; distributed collaboration is another topic.

---

## DD-09 · Data and brand boundary

**Decision**: All synthetic data; brand is fictional Qingshu Mobility; no real customer names, contracts, tickets, or recordings in repo.

**Rationale**: Portfolio compliance and public GitHub.

---

## DD-10 · Acceptance storylines are non-negotiable

**Decision**:

1. **Story1**: Skill writes `AIOutput` via Write/Govern  
2. **Story2**: Separate run of Plan Skill (e.g. `renewal_plan`) reads shared tags and blocks bad outreach  

**Rationale**: Without Story2, “anti-AI-silo” is slogans only.

---

## DD-11 · Wording boundary

**OK**: Fictional enterprise platform Loops+Tools+Skills reference implementation and demo recordings.  
**Not OK**: Claim shipped enterprise AI hub / multi-department production delivery.

---

## Superseded decisions (do not cite)

| Old decision | Status |
|--------------|--------|
| Phase-1 platform main list must treat all 6 Agent types as first-class loops | **Superseded** (see DD-03) |
| Main narrative “many brains per demo” vs “platform owns loops and tools” | **Superseded** (see DD-01/02) |
| Anti-AI-silo mainly via “shared Agent” | **Superseded** (see DD-02) |
| Default cross-function via Agent→Agent chat/pipeline | **Superseded** (see DD-06 / DD-12) |

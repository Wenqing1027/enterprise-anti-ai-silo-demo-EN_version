# Consulting narrative (Qingshu Mobility · Anti-AI-Silo)

> Version: V2.0 · 2026-08-06  
> Companion: [BLUEPRINT.md](../BLUEPRINT.md) · [Design decisions](./design-decisions.md)

---

## Pain points

Each department builds its own Agents, copies data access and half-loops → **AI silos ≈ data silos**.  
“One shared enterprise Agent” does not fix it: duplication is in **loops and tools**, while business variance hides in persona Prompts and cannot be governed.

---

## Position (how to explain to clients)

Enterprise AI delivery is three parts:

1. **Control Loops (platform)** — limited cognitive execution modes (this demo: **4**)  
2. **Tools (platform)** — unified tool ledger and approval boundaries (this demo: **3 classes**)  
3. **Skills (departments)** — department-built function plugins bound to a loop and approved tools  

Cross-department / cross-function work uses **shared semantics and AI output assets**: each function is an independent Skill, **one run at a time**; no Agent chat, no copying others’ private stores.

---

## UI split

| Page | For whom | Purpose |
|------|----------|---------|
| `/business` | Business departments | One function = one Skill try-run |
| `/ops` | Tech ops | Troubleshooting (logs / metrics / traces), **not** policy Q&A or a second Skill wall |

---

## Phased rollout (consulting framing)

| Phase | Focus |
|-------|-------|
| First | Platform four-loop skeleton + three-class tool governance + shared tags/`AIOutput`/capability catalog |
| Next | Departments mount Skills in bulk; flows document sequential and consumption relations |
| Later | Strengthen Plan runtime, eval, audit; split Vision etc. as needed |

Portfolio demo: Retrieve / Act / Extract runnable; Plan is contract + Story2 gate semantics (runtime can continue later).

---

## Within and across departments

- **One function = one Skill**: pick function = pick Skill; do not “pass” results to another Agent mid-run  
- **Cross-function**: later Skill reads shared layer only; relations in `docs/planning/`, `department_flows.json` (spec, not chained run)

---

## Anti-patterns (reject on the spot)

- One mega System Prompt as “enterprise brain”  
- Per-department isolated Agent + DataFetcher stacks  
- Claim “shared Agent” equals anti-AI-silo  
- Multi-Agent chat / Agent→Agent pipeline as main collaboration path  
- Single Orchestrator for all company flows  

---

## One-line close

**Platform owns loops and tools, departments deliver Skills, shared layer connects outputs — that is governable Anti-AI-Silo.**

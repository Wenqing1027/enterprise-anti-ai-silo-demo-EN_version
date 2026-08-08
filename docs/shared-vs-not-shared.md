# What the platform owns / does not own

> Version: V2.0 · 2026-08-06  
> Replaces old “shared vs not shared” short table; see [Design decisions](./design-decisions.md) · [BLUEPRINT](../BLUEPRINT.md)

---

## Platform-managed (release · allowlist · audit conventions)

| Object | Notes |
|--------|-------|
| **4 control loops** | Retrieve / Act / Extract / Plan implementation and version |
| **3 tool classes** | Read · Knowledge · Write/Govern; single ToolRegistry |
| **DataFetcher** | Single data access implementation |
| **Shared assets** | Unified IDs/models, tag dictionary, `AIOutput`, CapabilityCatalog |
| **Composition contract format** | `department_flows` fields and `via` conventions |
| **Run / log format** | Cross-loop reconciliation (demo level) |

---

## Department-built (platform does not write business logic)

| Object | Notes |
|--------|-------|
| **Skill** | **One function = one Skill**; goal, success criteria, tone, tool allowlist, schema/index slots |
| **Department function list** | Which Skills to mount; flows only declare shared dependencies (not chained run) |
| **Business copy and strategy** | e.g. service reassurance ≠ tele-sales tone (do not mix in one Skill) |

---

## Explicitly not shared / forbidden

| Forbidden | Reason |
|-----------|--------|
| Per-department control loop copies | Platform loops must be single implementation |
| Private DataFetcher / private tool impl per department | Silos and drift |
| Agent chat / Agent→Agent pipeline | Hard to govern; cross-function via shared output + new run only |
| “Shared Agent persona” as anti-AI-silo | Wrong object (see DD-02) |
| Single Orchestrator replacing four loops or chaining all Skills | Slides toward mega brain |

---

## Quick reference

```text
Platform: Loops(4) + Tools(3 classes) + Store/semantics
Departments: Skills(N) + declared flows
Cross-department: read/write AIOutput and unified tags only
```

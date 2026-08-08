# Planning · Module 3: Machine-readable contract and catalog wiring

> **Core reference · Module 3**  
> Source of truth: `data/entities/department_flows.json` (hand-maintained; generation script must not overwrite)  
> Skill loop mapping: `apps/skill_loops.py` · `data/entities/skill_loop_map.json`  
> Exposure: `apps/catalog.py` · `GET /v1/flows` · `GET /v1/departments/{id}/flows`  
> Version: V2.1 · 2026-08-07

---

## 1. JSON top level

```json
{
  "version": "v2",
  "description": "…each node = independently runnable Skill/function…",
  "node_kinds": ["skill", "placeholder", "store_read", "store_write"],
  "control_loops": ["retrieve", "act", "extract", "plan"],
  "flows": [ /* Flow objects */ ]
}
```

| Field | Type | Notes |
|-------|------|-------|
| `version` | string | Contract version, currently `v2` |
| `flows` | array | In-department function relationship flows |

---

## 2. Flow object

| Field | Required | Notes |
|-------|----------|-------|
| `flow_id` | ✅ | Globally unique |
| `department_id` | ✅ | Aligns with `apps.catalog.DEPARTMENTS` |
| `name` | ✅ | Human-readable name |
| `demo_ready` | ✅ | Aligns with demo Story |
| `nodes` | ✅ | Node list |
| `edges` | ✅ | Edge list (may be empty) |
| `parallel_groups` | ✅ | Parallel groups (may be empty) |
| `feature_ids` | | Linked business feature IDs |
| `notes` | | Human notes |

---

## 3. Node (function relationship spec)

**Node = one independently runnable function Skill** (or shared read/write / placeholder), **not** “one step in an Agent pipeline.”

| Field | Notes |
|-------|-------|
| `node_id` | Unique within flow |
| `kind` | `skill` · `placeholder` · `store_read` · `store_write` |
| `skill_id` | Optional; required intent for `skill` / some `placeholder` |
| `control_loop` | `retrieve` \| `act` \| `extract` \| `plan` (`store_*` null) |
| `label` | Short human label |
| `extension_type` | Optional: `rule_llm` / `vision` (kept after mapping to parent loop) |
| `note` | Optional note |

> Compatibility: if catalog still sees legacy `kind: agent_type` / `agent_type: rag`, it normalizes to `kind: skill` + `control_loop`.

---

## 4. Edge

| Field | Notes |
|-------|-------|
| `from` · `to` | `node_id` |
| `mode` | `sequence` = **data dependency** (usually via shared layer, two independent runs); `parallel` = independently demoable |
| `via` | Shared contract: `AIOutput` · `tag_id:…` · `payload_schema:…` |

This is **not** Extract Agent finishing and handing off to Act Agent.

---

## 5. Parallel group

```json
{ "group_id": "pg_prep", "node_ids": ["n1", "n2"], "label": "Parallel optional functions" }
```

---

## 6. Skill loop mapping

| Layer | Mapping |
|-------|---------|
| `skill.yaml` | Canonical `control_loop:` (retrieve\|act\|extract\|plan); RAG also keeps `agent_type: rag` for loader |
| Ledger | `apps/skill_loops.py` · `data/entities/skill_loop_map.json` |
| Public API | `GET /v1/skills` → each entry includes `control_loop` |
| flows nodes | `control_loop` matches skill ledger |
| FEATURES | `agent_type` uses canonical loop names (same as control_loop) |

Phase 1 shipped:

| control_loop | skill_id |
|--------------|----------|
| retrieve | `repair_kb` · `policy_kb` · `hr_rules` |
| act | `fill_ticket` · `crm_lookup` · `channel_ops` · `shared_write` |
| extract | `ticket_fields` · `voc_entities` · `voc_tagging` |
| plan | `renewal_plan` (Story2 / user_ops_renewal_gate) |

`# flow: <flow_id>` comments still reference orchestration flows.

### Run API (B3)

| Entry | Notes |
|-------|-------|
| `POST /v1/planning/runs` | Plan-specific (UI / ops main path) |
| `POST /v1/runs` | Unified entry: `control_loop=plan` (or `agent_type=planning` / inferred from feature·skill) |
| `GET /v1/planning/runs/{run_id}` | Step log replay |

Machine-readable: `/v1/meta` → `unified_runs_api`, `legacy_api_paths.plan`; `data/entities/control_loop_aliases.json`.

All four loops normalize responses to **RunResult** (Phase D): see [docs/run-result.md](../run-result.md); `GET /v1/meta` → `run_result`.

---

## 7. Maintenance

- **Hand-maintain** `department_flows.json`  
- `scripts/generate_synthetic_data.py` **must not** overwrite this file  
- New Skill: sync `control_loop` field + `skill_loops.py` + related flow nodes  

---

## 8. Quick acceptance

```bash
python3 -c "
from apps.catalog import list_flows, get_flow
from apps.skill_dispatch import load_skill_public
from apps.skill_loops import SKILL_CONTROL_LOOPS

fs = list_flows()
assert any(f['flow_id']=='service_ticket_to_shared' and f['demo_ready'] for f in fs)
n = get_flow('service_ticket_to_shared')['nodes'][0]
assert n['kind']=='skill' and n['control_loop'] in {'retrieve','act','extract','plan'}
assert load_skill_public('fill_ticket')['control_loop']=='act'
assert len(SKILL_CONTROL_LOOPS)==10
print('A3 OK', 'flows', len(fs))
"
```

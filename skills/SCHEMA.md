# skill.yaml format contract

This repo has **four** Skill YAML types (matching the platform's four control loops):

| Type | Identification | Loop `control_loop` | Loader |
|------|----------------|---------------------|--------|
| **Act (ReAct)** | Has `allowed_tools`, no `payload_schema`, not Retrieve/Plan | `act` | `agents/react/skill_loader.py` |
| **Extract** | Has `payload_schema` | `extract` | `agents/extraction/skill_loader.py` |
| **Retrieve (RAG)** | `control_loop: retrieve` or `agent_type: rag` + `kb_domains_allow` | `retrieve` | `agents/rag/skill_loader.py` |
| **Plan** | `control_loop: plan` or `agent_type: planning` | `plan` | `agents/planning/skill_loader.py` |

Routing: `apps/skill_dispatch.py` (`peek_skill_kind`).  
Loop registry: `apps/skill_loops.py` · `data/entities/skill_loop_map.json`.

---

## Common fields (all types)

| Field | Required | Description |
|-------|----------|-------------|
| `skill_id` | ✅ | Must match the directory name |
| `control_loop` | ✅ (recommended) | `retrieve` \| `act` \| `extract` \| `plan`; inferred by loader/registry if missing |

---

## ReAct (Act) fields

Single implementation: `agents/react/skill_schema.py` → `SkillConfig` (Pydantic validation on load).

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `skill_id` | ✅ | string | Must match directory name |
| `control_loop` | | `act` | Platform control loop |
| `department` | | string | Department narrative |
| `goal` | ✅ | string | One-line task goal |
| `success_hint` | | string | Human-readable success criteria |
| `success_when` | | enum | `wrote_ai_output` / `master_lookup` / `channel_lookup` / `none` |
| `max_steps` | | int 1–32 | Max tool steps (default 8) |
| `tone.label` / `tone.style` | ✅ | string | Tone/style |
| `tone.forbid` | | string | Forbidden items |
| `allowed_tools` | ✅ | string[] | Tool allowlist |
| `system_extra` / `output_format` | | string | Prompt supplements |
| `security` | | object | Security slot |

### `security` subfields

| Field | Default | Description |
|-------|---------|-------------|
| `kb_domains_allow` | `[]` | If non-empty, restricts `search_kb.domain` |
| `max_tool_calls_per_step` | `6` | Max tool_calls per turn |
| `redact_pii_in_observation` | `true` | Redact before replay |
| `block_on_outreach` | `false` | Hard stop on outreach block |
| `prompt_forbid_extra` | `""` | Additional prohibitions |

### System Prompt section order

`A_base` → `B_tone` → `C_goal` → `C2_system_extra` → `D_tools` → `E_output` → `F_security`

---

## RAG (Retrieve) fields (summary)

Implementation: `agents/rag/skill_schema.py` → `RagSkillConfig`.

| Field | Required | Description |
|-------|----------|-------------|
| `control_loop` | | Must be `retrieve` |
| `agent_type` | ✅ | Legacy identifier, still `rag` |
| `kb_domains_allow` | ✅ | Non-empty domain allowlist |
| `top_k` / `max_context_chars` | | Retrieval and context budget |
| `cite_required` | | Final answer must include citations |
| `success_when` | | `cited_answer` / `none` |
| `allowed_tools` | | For catalog |

Phase 1: `repair_kb` · `policy_kb` · `hr_rules`. See [docs/rag/06](../docs/rag/06-rag-skill-contract.md).

---

## Extraction (Extract) fields (summary)

| Field | Required | Description |
|-------|----------|-------------|
| `control_loop` | | `extract` |
| `payload_schema` | ✅ | `ticket_draft_v1` / `voc_entities_v1` |
| `write_ai_output` / `consumer_allow` | | Assetization |

Phase 1: `ticket_fields` · `voc_entities` · `voc_tagging`.

---

## In-department orchestration (flow) — functional relationship spec

Machine-readable source of truth: `data/entities/department_flows.json` (see [docs/planning/03](../docs/planning/03-module-3-machine-readable-contract-and-catalog.md)).

- **Nodes** = independently runnable Skills/features (or shared-layer points), **not** Agent pipelines  
- `mode: sequence` = data dependency (two independent runs, via shared layer)  
- `mode: parallel` = can be demo'd independently  

YAML header comments may still reference: `# flow: service_ticket_to_shared`.

| skill_id | control_loop | Relationship |
|----------|--------------|--------------|
| `fill_ticket` | act | `produces_for: [renewal_plan, voc_tagging]` |
| `ticket_fields` | extract | ∥ optional parallel to `fill_ticket` for same goal |
| `voc_tagging` / `voc_entities` | extract | Write to shared; cross-dept only via `AIOutput` |
| `renewal_plan` | plan | Story2 / `user_ops_renewal_gate`; `consumes_from` upstream; gate + short plan in one run |
| `repair_kb` | retrieve | Exists **in parallel** with Story1 |
| `policy_kb` | retrieve | **Optional parallel** to order-review demo |
| `hr_rules` | retrieve | Standalone Q&A flow |
| `crm_lookup` / `channel_ops` / `shared_write` | act | Lookup / channel / shared write |

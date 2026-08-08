# RAG · Skill contract (R3)

> **Core reference · RAG R3**  
> Control loop was planned (R4); this step delivers loadable `skill.yaml` + Pydantic schema + dispatch  
> Version: V1.0 · 2026-08-05

---

## 1. Scope

| Item | Notes |
|------|-------|
| In scope | Machine-readable RAG Skill contract; mount `repair_kb` / `policy_kb` / `hr_rules` |
| Out of scope | `retrieve→stuff→generate` runtime (R4) |
| vs R2 | Skill declares `kb_domains_allow`; retrieval still uses wired `search_kb` / TF-IDF |

---

## 2. Identification and dispatch

```text
payload_schema?     → Extraction
agent_type: rag     → RAG
else                → ReAct
```

Implementation: `apps/skill_dispatch.peek_skill_kind` / `load_skill_public`.

---

## 3. Phase-1 three Skills

| skill_id | Domain | Department | Features |
|----------|--------|------------|----------|
| `repair_kb` | repair | Service | F-SVC-002/004 · F-UO-009 |
| `policy_kb` | policy | Order/policy | Policy copy Q&A |
| `hr_rules` | hr | HR | F-HR-001/003 |

Paths:

- `skills/repair_kb/skill.yaml`
- `skills/policy_kb/skill.yaml`
- `skills/hr_rules/skill.yaml`
- Schema: `agents/rag/skill_schema.py`
- Loader: `agents/rag/skill_loader.py`

---

## 4. Key fields

| Field | Required | Notes |
|-------|----------|-------|
| `agent_type` | ✅ | `rag` |
| `kb_domains_allow` | ✅ | Non-empty; dual gate with `security.kb_domains_allow` |
| `top_k` | | Default 5 |
| `max_context_chars` | | Stuff budget, default 2400 |
| `cite_required` | | Final answer must cite |
| `success_when` | | `cited_answer` |
| `allowed_tools` | | catalog / docs; loop uses DataFetcher directly |
| `tone` / `system_extra` / `output_format` | | Prompt slots (R4 consumes) |

Prompt section order: `RAG_PROMPT_SECTION_ORDER` (A_base…F_security).

---

## 5. Acceptance

```bash
python -c "
from apps.skill_dispatch import peek_skill_kind, load_skill_public, list_skill_ids
assert peek_skill_kind('repair_kb')=='rag'
assert peek_skill_kind('policy_kb')=='rag'
assert peek_skill_kind('hr_rules')=='rag'
assert peek_skill_kind('fill_ticket')=='react'
assert peek_skill_kind('ticket_fields')=='extraction'
for sid in ('repair_kb','policy_kb','hr_rules'):
    p=load_skill_public(sid)
    assert p['agent_kind']=='rag' and p['kb_domains_allow']
print('skills', [s for s in list_skill_ids() if peek_skill_kind(s)=='rag'])
"
python scripts/smoke_rag_skills.py
```

---

## 6. Next steps

**R4 control loop** ✅ — see [07-control-loop-implementation-and-wiring](./07-control-loop-implementation-and-wiring.md).

Optional next: **R5 gold eval set** / catalog UI tuning.

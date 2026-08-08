# RAG · R7 Orchestration writeback and gap review

> Version: V1.0 · 2026-08-05  
> Trigger: completeness check after `department_flows` RAG writeback

---

## 1. R7 written back

| flow_id | demo_ready | skill | Related FEATURES |
|---------|------------|-------|------------------|
| `service_repair_qa` | ✅ | `repair_kb` | F-SVC-002 / F-SVC-004 |
| `user_ops_app_qa` | ✅ | `repair_kb` | F-UO-009 |
| `order_policy_qa` | ✅ | `policy_kb` | F-POL-RAG |
| `hr_policy_qa` | ✅ | `hr_rules` | F-HR-001 |
| `channel_ops_board` | ❌ (half-ready) | ReAct `channel_ops` ∥ RAG `policy_kb` | Merge still planned |

Synced: `docs/planning/02` · `docs/rag/02` · catalog `flow_ids` · README · `agent-orchestration.md`.

---

## 2. Phase-1 RAG checklist review (R0–R8)

| Step | Status | Notes |
|------|--------|-------|
| R0 planning doc trio | ✅ | `docs/rag/01–03` |
| R1 chunking | ✅ | `chunks.json` |
| R2 index / `search_kb` | ✅ | `tfidf_index.json` |
| R3 Skill contract | ✅ | Three YAML + loader |
| R4 control loop | ✅ | CLI / `POST /v1/rag/runs` |
| R5 gold-standard + smoke | ✅ | 15 cases PASS |
| R6 Catalog / UI | ✅ | Demo cards + business/ops routing |
| R7 orchestration contract | ✅ | This step |
| R8 side-path `write_ai_output` | ⏸ | **Intentionally not done** (not Story1/2 hard dependency) |

---

## 3. Known gaps (not accidental omissions; out of scope / phase 2)

| Item | Ruling |
|------|--------|
| `channel_kb` / `product_kb` Skills | Not built; channel flow reuses `policy_kb` |
| Channel board auto-merge | Planning node still placeholder |
| RAG → AIOutput assetization | R8 optional, not implemented |
| KB auto-update pipeline | Extraction→store, phase 2 |
| embedding / rerank | Phase 1 stays TF-IDF |
| `parallel_orthogonal` orch copy on business wall | Partial label mapping; empty default OK |
| Recording script missing RAG segment | Can add 30–60s later |

---

## 4. Acceptance command

```bash
python3 -c "
from apps.catalog import list_flows, get_flows_by_department
fs = list_flows()
need = {'service_repair_qa','user_ops_app_qa','order_policy_qa','hr_policy_qa'}
ids = {f['flow_id'] for f in fs}
assert need <= ids
assert any(f['flow_id']=='service_repair_qa' and f['demo_ready'] for f in fs)
ch = [f for f in fs if f['flow_id']=='channel_ops_board'][0]
assert any(n.get('skill_id')=='policy_kb' for n in ch['nodes'])
print('flows', len(fs), 'rag_demo', sorted(need))
"
```

# RAG gold-standard eval and smoke (R5)

> **Core reference · RAG R5**  
> Gold set: `data/eval/rag/gold_qa.json`  
> Eval: `scripts/eval_rag.py`  
> Smoke: `scripts/smoke_rag.py` (core + 1 cross-domain)  
> Reports: `docs/rag/eval_reports/`  
> Version: V1.0 · 2026-08-05

---

## 1. Thresholds

| Metric | Threshold | Meaning |
|--------|-----------|---------|
| `run_ok_rate` | 100% | Control loop returns successfully |
| `hit_doc_recall` | ≥80% | expect_hit cases: citation hits gold `doc_id_any_of` |
| `cite_present_rate` | 100% | expect_hit cases must have citations |
| `keyword_hit_rate` | ≥70% | Answer contains one of `must_contain_any` |
| `domain_isolation_rate` | 100% | Citation domains ⊆ Skill `kb_domains_allow` |
| `cross_domain_safe_rate` | 100% | Cross-domain: no forbidden doc leak + answer admits gap/guides |

---

## 2. Gold set structure

15 cases: `core` 3 + `extended` 9 + `cross_domain` 3.

```bash
# Smoke (~4 LLM calls)
python scripts/smoke_rag.py

# Full eval
python scripts/eval_rag.py
# python scripts/eval_rag.py --suite core
# python scripts/eval_rag.py --limit 3
```

Reports:

- `docs/rag/eval_reports/latest.md`
- `docs/rag/eval_reports/latest.json`
- `docs/rag/eval_reports/eval-<timestamp>.*`

---

## 3. UI smoke notes

| Entry | Behavior |
|-------|----------|
| Business wall RAG demo card | `POST /v1/rag/runs` (`business.js` routed) |
| Ops `/ops?agent_type=rag` | Lists RAG Skills; try-run uses `/v1/rag/runs` |

---

## 4. Acceptance checklist

- [x] Gold set ≥ core 3 Q + cross-domain  
- [x] `eval_rag.py` + reports on disk  
- [x] `smoke_rag.py` fast path  
- [x] Business wall / ops RAG API routing  

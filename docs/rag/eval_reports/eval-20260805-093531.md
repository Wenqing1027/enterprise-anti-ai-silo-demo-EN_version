# RAG gold-standard eval report · 2026-08-05T09:35:31Z

- **Result**: `PASS`
- **Case count**: 15
- **Duration**: 51.03s

## Metrics

| Metric | Value | Threshold |
|--------|-------|-----------|
| Run success rate (`run_ok_rate`) | 1.0 | 1.0 |
| Gold doc recall (`hit_doc_recall`) | 1.0 | 0.8 |
| Citation present rate (`cite_present_rate`) | 1.0 | 1.0 |
| Keyword coverage (`keyword_hit_rate`) | 1.0 | 0.7 |
| Domain isolation (`domain_isolation_rate`) | 1.0 | 1.0 |
| Cross-domain safety (`cross_domain_safe_rate`) | 1.0 | 1.0 |

## Per case

| id | skill | ok | doc_hit | kw | xdom | stop |
|----|-------|----|---------|----|------|------|
| RAG-REP-001 | repair_kb | True | True | True | None | cited_answer |
| RAG-REP-002 | repair_kb | True | True | True | None | cited_answer |
| RAG-REP-003 | repair_kb | True | True | True | None | cited_answer |
| RAG-REP-004 | repair_kb | True | True | True | None | cited_answer |
| RAG-REP-005 | repair_kb | True | True | True | None | cited_answer |
| RAG-POL-001 | policy_kb | True | True | True | None | cited_answer |
| RAG-POL-002 | policy_kb | True | True | True | None | cited_answer |
| RAG-POL-003 | policy_kb | True | True | True | None | cited_answer |
| RAG-POL-004 | policy_kb | True | True | True | None | cited_answer |
| RAG-HR-001 | hr_rules | True | True | True | None | cited_answer |
| RAG-HR-002 | hr_rules | True | True | True | None | cited_answer |
| RAG-HR-003 | hr_rules | True | True | True | None | cited_answer |
| RAG-XDOM-001 | repair_kb | True | None | True | True | no_hit_answered |
| RAG-XDOM-002 | policy_kb | True | None | True | True | cited_answer |
| RAG-XDOM-003 | hr_rules | True | None | True | True | no_hit_answered |

# Extraction · Phase 4: Gold-standard eval + UI wiring

> **Implementation doc · Extraction Phase 4** (depends on [Phase 3](./03-phase-3-control-loop-implementation-and-wiring.md))  
> Version: V1.0 · 2026-08-05  
> Goal: ≥20+20 gold cases aligned with Phase 1 thresholds; business/ops UI routes by `agent_type` to Extraction API.

---

## 1. Deliverables

| Item | Path |
|------|------|
| Ticket fill gold set (50 cases) | `data/eval/extraction/gold_ticket_fields.json` |
| VoC gold set (50 cases) | `data/eval/extraction/gold_voc_entities.json` |
| Eval script | `scripts/eval_extraction.py` |
| Report dir | `docs/extraction/eval_reports/` (`latest.md` / `latest.json`) |
| UI routing | `apps/ui/business.js`, `apps/ui/ops.js` |
| JSON enforcement | Extraction DeepSeek calls use `response_format=json_object` |

---

## 2. Thresholds (same as Phase 1)

### ticket_fields

| Metric | Threshold |
|--------|-----------|
| Schema compliance | 100% |
| ticket_type | ≥80% |
| fault_category (fault subset) | ≥75% |
| tag_id Top-1 (incl. accept set) | ≥75% |
| Missed block | 0 |
| sentiment | ≥80% (non-complaint allows one-grade `neu↔neg` tolerance for acceptance) |
| ID recall (when explicit) | ≥95% |

### voc_entities

| Metric | Threshold |
|--------|-----------|
| Schema compliance | 100% |
| tag_id | ≥80% |
| Missed block | 0 |
| sentiment | ≥85% |
| tag_domain | ≥90% |
| Out-of-vocabulary tag rate | ≤5% |

Eval uses `write_output=false` to avoid polluting shared outputs; block tags count via primary or `secondary_tag_ids`.

---

## 3. How to run eval

```bash
source .venv/bin/activate
python scripts/eval_extraction.py
# Debug limit:
# python scripts/eval_extraction.py --limit 3
# python scripts/eval_extraction.py --ticket-only
```

Exit code `0` = both suites pass; reports written to:

- `docs/extraction/eval_reports/latest.md`
- `docs/extraction/eval_reports/eval-<timestamp>.md`

---

## 4. UI / API routing

| Entry | Behavior |
|-------|----------|
| Business wall `F-SVC-001-EXT` / `F-VOC-002` | `POST /v1/extraction/runs` |
| Business wall ReAct demo | Still `POST /v1/react/runs` |
| Ops `/ops?agent_type=extraction` | Lists Extraction Skills only; try-run uses Extraction API |
| Ops `/ops?agent_type=react` | Lists ReAct Skills only |

---

## 5. Phase 4 acceptance

- [x] Gold sets ≥20 each  
- [x] Eval script + reports on disk  
- [x] UI routes by agent_type  
- [x] `response_format=json_object`  
- [x] `latest.md` actual **PASS** (ticket/voc 50 each)

Expanded summary (`eval_reports/latest.md`):

| Suite | n | Schema | Key accuracy | Missed block |
|-------|---|--------|--------------|--------------|
| ticket_fields | 50 | 100% | type 86% / fault 86.4% / tag 98% / sentiment tolerance 100% | 0 |
| voc_entities | 50 | 100% | tag 100% / sentiment 92% / domain 100% | 0 |

---

## 6. Revision history

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-05 | Gold sets, eval, UI, json_object |
| V1.1 | 2026-08-05 | Expanded gold to 50 each and re-ran |
| V1.2 | 2026-08-05 | Dual-page wiring + parallel/sequential notes |

---

## 7. Web wiring

Dual-page wiring and parallel/sequential notes: [docs/agent-orchestration.md](../agent-orchestration.md) and [docs/react/05-module-5-ui-principles-integration-api.md](../react/05-module-5-ui-principles-integration-api.md).

- Business: `/business` (Extraction demo runnable; non-demo display + orchestration notes)  
- Ops: `/ops?agent_type=extraction`

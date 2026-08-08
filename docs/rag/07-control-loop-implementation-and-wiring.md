# RAG · Control loop implementation and wiring (R4)

> **Core reference · RAG R4**  
> Control loop: `retrieve → stuff → generate` (+ citations)  
> LLM: DeepSeek (`profile=rag` → `DEEPSEEK_RAG_API_KEY` falls back to `DEEPSEEK_API_KEY`)  
> Version: V1.0 · 2026-08-05

---

## 1. Implementation map

| Path | Role |
|------|------|
| `agents/rag/agent.py` | Control loop |
| `agents/rag/prompts.py` | System / user assembly |
| `apps/cli.py --agent-type rag` | CLI |
| `POST /v1/rag/runs` | API |
| `scripts/smoke_rag.py` | End-to-end smoke |

---

## 2. Environment variables

```bash
# .env (do not commit)
DEEPSEEK_RAG_API_KEY=sk-...
# or fallback
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_RAG_MODEL=deepseek-chat
DEEPSEEK_RAG_TEMPERATURE=0.2
```

---

## 3. Run

```bash
python apps/cli.py --agent-type rag --skill repair_kb \
  --input '{"query":"Range below rated — how to troubleshoot?"}'

python scripts/smoke_rag.py
```

API:

```bash
curl -s localhost:8000/v1/rag/runs -H 'Content-Type: application/json' \
  -d '{"skill_id":"repair_kb","input":{"query":"Range below rated — how to troubleshoot?"}}'
```

---

## 4. Step semantics

| phase | Behavior |
|-------|----------|
| retrieve | `DataFetcher.search_kb`, domain = `kb_domains_allow` |
| stuff | Fill segments up to `max_context_chars` |
| generate | DeepSeek final answer |
| cite / cite_backfill | Validate or backfill `kb_chunk_id` citations |

Success: `stop_reason=cited_answer` (hits) or `no_hit_answered` (allowed no-hit explanation).

---

## 5. Demo function cards

`F-SVC-002` / `F-SVC-004` / `F-POL-RAG` / `F-UO-009` / `F-HR-001` → `demo_ready`, mapped to Skills.

Next: **R5 gold eval** — see [08-gold-standard-eval-and-smoke](./08-gold-standard-eval-and-smoke.md) (PASS).

# RAG · Index and retriever (R2)

> **Core reference · RAG R2**  
> Input: `data/knowledge/chunks.json`  
> Output: `data/knowledge/tfidf_index.json`  
> Impl: `shared/rag/tfidf_index.py` · `shared/rag/tokenize.py`  
> Build: `scripts/build_kb_index.py`  
> Single exit: `DataFetcher.search_kb` / `get_kb_chunk` (Tool `search_kb` unchanged)  
> Version: V1.0 · 2026-08-05

---

## 1. Goal

Build a persisted, re-runnable retrieval index on chunks so:

1. RAG control loop and ReAct tools share the same `search_kb`  
2. Hits return **stable** `kb_chunk_id` + chunk body (not temp `#chunk{i}`)  
3. Phase 1 **zero heavy deps** (pure Python TF-IDF, no numpy/sklearn required)

---

## 2. Index design

| Item | Choice |
|------|--------|
| Algorithm | TF-IDF + cosine similarity |
| Tokenization | Whitespace + CJK 2/3-char n-grams (`shared/rag/tokenize.py`) |
| Title boost | `title` / `section_path` terms × `title_boost` (default 1.35) |
| Domain filter | `domain=` filters `kb_domain` before scoring |
| `index_id` | `tfidf_charngram_v1` |

Not building: production ANN, embedding API, per-department index files (domain is a field filter, not separate DBs).

---

## 3. On-disk layout

| Path | Role |
|------|------|
| `data/knowledge/chunks.json` | R1 chunk input |
| **`data/knowledge/tfidf_index.json`** | **R2 index output (vocab + idf + sparse vectors + chunk bodies)** |
| `docs/rag/05-index-and-retriever.md` | This doc |
| `scripts/build_kb_index.py` | Build entry |
| `scripts/smoke_kb_index.py` | Smoke test |

Maintenance: `generate_synthetic_data.py` **must not** overwrite `tfidf_index.json`. After source md or chunks change:

```bash
python scripts/build_kb_chunks.py
python scripts/build_kb_index.py
```

---

## 4. `tfidf_index.json` structure (summary)

```json
{
  "version": "v1",
  "index_id": "tfidf_charngram_v1",
  "built_at": "ISO-8601",
  "source_chunks": "knowledge/chunks.json",
  "params": { "ngram_ns": [2, 3], "title_boost": 1.35 },
  "stats": { "chunks": 38, "vocab_size": N, "by_domain": {} },
  "vocab": ["term0", "term1", "..."],
  "idf": [1.2, 1.1, "..."],
  "docs": [
    {
      "kb_chunk_id": "repair__range-troubleshooting#c0002",
      "kb_doc_id": "repair__range-troubleshooting",
      "kb_domain": "repair",
      "title": "Range troubleshooting",
      "section_path": "… › 1. Symptom check",
      "content": "…",
      "norm": 3.14,
      "tfidf": { "12": 0.88, "45": 0.42 }
    }
  ]
}
```

---

## 5. Runtime wiring

```text
Tool search_kb
    → DataFetcher.search_kb
        → KnowledgeSource.search_chunks
            → TfidfIndex.search  (fallback keyword scan of chunks.json if index missing)
```

| API | Behavior |
|-----|----------|
| `search_kb(q, domain, top_k)` | Returns `KbChunk` list: real `kb_chunk_id` + chunk `content` + `kb_score` |
| `get_kb_chunk(id)` | Read chunk by id (citation expand) |
| `get_kb_document(doc_id)` | Still returns full md (`#full`) |

---

## 6. Acceptance

```bash
python scripts/build_kb_index.py
python scripts/smoke_kb_index.py
python scripts/smoke_datafetcher.py
```

Expect: repair range questions, policy rebate questions, HR SOP questions hit in-domain top; `kb_chunk_id` contains `#c`.

---

## 8. Two judgments (2026-08-05)

| Claim | Ruling |
|-------|--------|
| “R3 is the real demo node; R2 not wired” | **Incorrect**. R2 wrote `tfidf_index.json`; `search_kb`/`smoke_kb_index` pass — **retrieval layer is demoable**. R3 is Skill **contract**; **Agent demo** needs R3+R4. R3 alone ≠ “wired end-to-end.” |
| “TF-IDF is not worth it in demo” | **Not true for this repo**. Blueprint says “local TF-IDF / avoid heavy deps”; gold Q&A hits correct docs in three domains. Low absolute scores are normal for n-gram cosine; **query-time phrase/title boost** improves UX; **not** switching to embedding heavy deps. |

Demo layers:

```text
R2 retrieval demo  ✅ (Tool / DataFetcher)
R3 Skill contract  ✅ (loadable config; this step)
R4 control loop    → true RAG Agent end-to-end Q&A
```

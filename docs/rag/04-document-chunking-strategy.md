# RAG · Document chunking strategy (R1)

> **Core reference · RAG R1 prerequisite**  
> Source docs: `data/knowledge/{repair,policy,hr,product,channel}/*.md`  
> Machine-readable output: `data/knowledge/chunks.json`  
> Build script: `scripts/build_kb_chunks.py`  
> Chunking impl: `shared/rag/chunking.py`  
> Version: V1.0 · 2026-08-05

---

## 1. Goal

Split synthetic long-form knowledge into retrievable, citable segments for later indexing (TF-IDF/vectors) and RAG control loop `retrieve`.

| Principle | Notes |
|-----------|-------|
| Source read-only | Do not edit `*.md` body; chunks are derived assets |
| Semantics first | Prefer Markdown `##` sections; avoid cutting step tables mid-way |
| Citable | Each chunk has stable `kb_chunk_id`; final answer can point back |
| Re-runnable | `python scripts/build_kb_chunks.py` regenerates; do not hand-edit JSON |
| Single exit | Retrieval still via DataFetcher / `search_kb` (R2 wires next) |

---

## 2. Chunking rules

### 2.1 Parameters (phase-1 defaults)

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `max_chunk_chars` | `520` | Max chunk size (~260–400 token scale for CJK) |
| `min_chunk_chars` | `48` | Short chunks merge with next (keep heading metadata) |
| `overlap_chars` | `64` | Window overlap only, keeps cross-segment context |
| `heading_levels` | `##` | Primary split; `#` title goes to doc-level `title`, not its own chunk |

### 2.2 Algorithm (ordered)

```text
1. Read index.json → locate md → full text
2. Drop first `#` title line, split by ##
3. For each section:
   - If length ≤ max_chunk_chars → one chunk for whole section
   - If too long → split by blank lines/paragraphs; still too long → fixed window + overlap
4. Merge adjacent short chunks (< min), merged size still ≤ max
5. Prefix chunk body with «doc title › section title» for retrieval and citation
6. Write chunks.json (with manifest stats)
```

### 2.3 ID conventions

| Field | Format | Example |
|-------|--------|---------|
| `kb_doc_id` | From index | `repair__range-troubleshooting` |
| `kb_chunk_id` | `{kb_doc_id}#c{nnnn}` | `repair__range-troubleshooting#c0001` |
| `section_path` | `Doc title › Section title` | `Range troubleshooting manual › 2. Quick triage` |
| `char_start` / `char_end` | UTF-8 char offset in **source full text** (approx.) | Debug only, not a hard gate |

`#c` index increments from `0001` **within one document**; stable order on re-run.

---

## 3. On-disk layout

| Path | Role |
|------|------|
| `data/knowledge/**/*.md` | Source docs (human read + generator seeds) |
| `data/knowledge/index.json` | Doc-level catalog (existing) |
| **`data/knowledge/chunks.json`** | **Chunk machine-readable truth (this step)** |
| `docs/rag/04-document-chunking-strategy.md` | This doc (human strategy) |
| `shared/rag/chunking.py` | Pure chunking functions for scripts and index |

**Do not**: let `scripts/generate_synthetic_data.py` overwrite `chunks.json` (same rule as `department_flows.json`: hand-maintained / dedicated scripts).

---

## 4. `chunks.json` schema (summary)

```json
{
  "version": "v1",
  "strategy_id": "heading_then_window_v1",
  "params": { "max_chunk_chars": 520, "min_chunk_chars": 48, "overlap_chars": 64 },
  "built_at": "ISO-8601",
  "source_index": "knowledge/index.json",
  "stats": { "docs": 15, "chunks": N, "by_domain": { "repair": … } },
  "chunks": [
    {
      "kb_chunk_id": "repair__range-troubleshooting#c0001",
      "kb_doc_id": "repair__range-troubleshooting",
      "kb_domain": "repair",
      "title": "Range troubleshooting",
      "section_heading": "1. Symptom check",
      "section_path": "Range troubleshooting › 1. Symptom check",
      "content": "…",
      "char_count": 123,
      "char_start": 0,
      "char_end": 123,
      "source_path": "knowledge/repair/range-troubleshooting.md"
    }
  ]
}
```

---

## 5. Acceptance

```bash
python scripts/build_kb_chunks.py
python -c "
import json
from pathlib import Path
p = Path('data/knowledge/chunks.json')
d = json.loads(p.read_text(encoding='utf-8'))
assert d['version']=='v1'
assert d['stats']['docs'] >= 15
assert d['stats']['chunks'] >= d['stats']['docs']
assert all(c['kb_chunk_id'] and c['content'].strip() for c in d['chunks'])
print('ok', d['stats'])
"
```

Next step: **R2 index** — see [05-index-and-retriever](./05-index-and-retriever.md) (`search_kb` wired).

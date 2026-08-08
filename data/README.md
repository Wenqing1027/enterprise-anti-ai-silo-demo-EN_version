# data/ Synthetic Data Guide

Brand: **Qingshu Mobility**  
Data seed: `20260801`  
Rebuild command: `python scripts/generate_synthetic_data.py`

## Compliance

- Fully synthetic; no real customers / contracts / ticket recordings
- All VINs use `QS0…` prefix
- Phone numbers are `phone_masked` only (middle four digits ****)
- Do not copy any real customer or OEM materials into the repo

## Directory

| Path | Contents |
|------|------|
| `OBJECT_CATALOG.md` | Noun / entity catalog |
| `vocab/field_glossary.json` | Cross-department field definitions |
| `vocab/tag_vocabulary.json` | Tag dictionary |
| `entities/*.json` | Structured entities (incl. `control_loop_aliases.json`, `tool_class_map.json`, `skill_loop_map.json`, `department_flows.json`) |
| `knowledge/**` | Unstructured long text (source md + `index.json`) |
| `knowledge/chunks.json` | RAG chunks (`scripts/build_kb_chunks.py`) |
| `knowledge/tfidf_index.json` | RAG TF-IDF index (`scripts/build_kb_index.py`) |
| `seeds/*.json` | Story1/2 demo seeds |
| `MANIFEST.json` | Scale stats and compliance statement |

Chunk / index docs: `docs/rag/04-chunking-strategy.md` · `docs/rag/05-index-and-retriever.md`. Rebuild:

```bash
python scripts/build_kb_chunks.py
python scripts/build_kb_index.py
```

## Scale (this build)

See `MANIFEST.json` for counts.

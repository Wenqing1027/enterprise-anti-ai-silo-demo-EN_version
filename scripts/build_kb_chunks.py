#!/usr/bin/env python3
"""Build data/knowledge/chunks.json from source docs.

Usage (repo root):
  python scripts/build_kb_chunks.py
  python scripts/build_kb_chunks.py --max-chars 520 --min-chars 48 --overlap 64
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.rag.chunking import ChunkParams, build_chunks_payload


def _load_documents(knowledge_dir: Path) -> list[dict]:
    index_path = knowledge_dir / "index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"Missing {index_path}")
    meta = json.loads(index_path.read_text(encoding="utf-8"))
    data_dir = knowledge_dir.parent
    docs: list[dict] = []
    for item in meta.get("documents", []):
        rel = item.get("path", "")
        file_path = data_dir / rel if rel.startswith("knowledge/") else knowledge_dir / Path(rel).name
        if not file_path.exists():
            domain = item.get("kb_domain", "")
            title = item.get("title", "")
            file_path = knowledge_dir / domain / f"{title}.md"
        if not file_path.exists():
            print(f"[warn] skip missing: {rel}", file=sys.stderr)
            continue
        content = file_path.read_text(encoding="utf-8")
        docs.append(
            {
                "kb_doc_id": item.get("kb_doc_id") or f"{file_path.parent.name}__{file_path.stem}",
                "kb_domain": item.get("kb_domain") or file_path.parent.name,
                "title": item.get("title") or file_path.stem,
                "path": rel or str(file_path.relative_to(data_dir)),
                "source_path": rel or str(file_path.relative_to(data_dir)),
                "content": content,
            }
        )
    return docs


def main() -> int:
    parser = argparse.ArgumentParser(description="Build knowledge chunks.json")
    parser.add_argument(
        "--knowledge-dir",
        type=Path,
        default=ROOT / "data" / "knowledge",
        help="Knowledge base root directory",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Output path (default: knowledge-dir/chunks.json)",
    )
    parser.add_argument("--max-chars", type=int, default=520)
    parser.add_argument("--min-chars", type=int, default=48)
    parser.add_argument("--overlap", type=int, default=64)
    args = parser.parse_args()

    knowledge_dir: Path = args.knowledge_dir
    out_path: Path = args.out or (knowledge_dir / "chunks.json")
    params = ChunkParams(
        max_chunk_chars=args.max_chars,
        min_chunk_chars=args.min_chars,
        overlap_chars=args.overlap,
    )

    documents = _load_documents(knowledge_dir)
    if not documents:
        print("No documents to chunk", file=sys.stderr)
        return 1

    payload = build_chunks_payload(
        documents=documents,
        params=params,
        source_index="knowledge/index.json",
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    stats = payload["stats"]
    print(f"wrote {out_path}")
    print(
        f"docs={stats['docs']} chunks={stats['chunks']} by_domain={stats['by_domain']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
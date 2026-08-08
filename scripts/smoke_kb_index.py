#!/usr/bin/env python3
"""R2 index smoke: TF-IDF on disk + DataFetcher.search_kb chunk hits."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shared.datafetcher import DataFetcher, KbChunk  # noqa: E402
from shared.rag.tfidf_index import TfidfIndex  # noqa: E402


def main() -> None:
    index_path = ROOT / "data/knowledge/tfidf_index.json"
    assert index_path.exists(), "Missing tfidf_index.json; run: python scripts/build_kb_index.py"

    idx = TfidfIndex.load(index_path)
    assert idx.meta.get("index_id") == "tfidf_charngram_v1"
    assert (idx.meta.get("stats") or {}).get("chunks", 0) >= 15
    assert len(idx.vocab) > 50

    # search
    direct = idx.search("How do I troubleshoot range below the rated value?", domain="repair", top_k=3)
    assert direct and direct[0].chunk.kb_domain == "repair"
    assert "range" in (direct[0].chunk.content or "").lower() or "range" in (direct[0].chunk.title or "").lower()

    policy = idx.search("2026Q3 pickup rebate tiers", domain="policy", top_k=3)
    assert policy and policy[0].chunk.kb_domain == "policy"

    hr = idx.search("agent quality check SOP red lines", domain="hr", top_k=3)
    assert hr and hr[0].chunk.kb_domain == "hr"

    # domain filter: query is repair-ish but domain=hr
    cross = idx.search("range anomaly troubleshooting", domain="hr", top_k=3)
    assert all(h.chunk.kb_domain == "hr" for h in cross)

    # DataFetcher
    fetcher = DataFetcher()
    hits = fetcher.search_kb("How do I troubleshoot range below the rated value?", domain="repair", top_k=3)
    assert hits and all(isinstance(h, KbChunk) for h in hits)
    assert hits[0].kb_chunk_id and "#c" in (hits[0].kb_chunk_id or "")
    assert hits[0].kb_score and hits[0].kb_score > 0
    assert hits[0].content and len(hits[0].content) > 20

    got = fetcher.get_kb_chunk(hits[0].kb_chunk_id or "")
    assert got is not None and got.kb_chunk_id == hits[0].kb_chunk_id

    print("OK kb index smoke")
    print(
        json.dumps(
            {
                "vocab_size": len(idx.vocab),
                "chunks": (idx.meta.get("stats") or {}).get("chunks"),
                "top_repair": {
                    "kb_chunk_id": hits[0].kb_chunk_id,
                    "score": hits[0].kb_score,
                    "title": hits[0].title,
                },
                "top_policy": {
                    "kb_chunk_id": policy[0].chunk.kb_chunk_id,
                    "score": policy[0].score,
                },
                "top_hr": {
                    "kb_chunk_id": hr[0].chunk.kb_chunk_id,
                    "score": hr[0].score,
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
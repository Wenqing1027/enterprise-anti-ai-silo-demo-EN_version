"""Supplemental types returned by DataFetcher (unified model layer, no source metadata)."""

from __future__ import annotations

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import KbDomain


class KbChunk(QingshuModel):
    """search （ domain， IO ）。"""

    kb_domain: KbDomain | str | None = Field(default=None, description="domain")
    kb_doc_id: str | None = Field(default=None, description="documentID")
    kb_chunk_id: str | None = Field(default=None, description="ID")
    title: str | None = Field(default=None, description="documentTitle")
    content: str | None = Field(default=None, description="")
    kb_score: float | None = Field(default=None, description="search 0-1")
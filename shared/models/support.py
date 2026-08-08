"""Data models · support (from standard-field-glossary)."""

from __future__ import annotations

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import ClauseRiskLevel, KbDomain, ProposalLevel

class Process(QingshuModel):
    """HR · Process. Fields from standard field table."""

    process_id: str | None = Field(
        default=None,
        description="Process ID. ID",
        json_schema_extra={"example": "PROC-"},
    )
    redundant_step: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "demo"},
    )
    bottleneck_step: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "demo"},
    )
    cycle_time_hours: float | None = Field(
        default=None,
        description="Week Duration.",
        json_schema_extra={"example": "72"},
    )
    proposal_level: ProposalLevel | None = Field(
        default=None,
        description=". L1|L2|L3",
        json_schema_extra={"example": "L2"},
    )

class HR(QingshuModel):
    """HR · HR. Fields from standard field table."""

    job_id: str | None = Field(
        default=None,
        description="ID.",
        json_schema_extra={"example": "JOB-"},
    )
    match_score: float | None = Field(
        default=None,
        description="Score. Score",
        json_schema_extra={"example": "84"},
    )

class Legal(QingshuModel):
    """HR · Legal. Fields from standard field table."""

    contract_id: str | None = Field(
        default=None,
        description="ID. ID",
        json_schema_extra={"example": "CT-2026-889"},
    )
    clause_risk_level: ClauseRiskLevel | None = Field(
        default=None,
        description="RiskLevel. low|medium|high",
        json_schema_extra={"example": "high"},
    )
    clause_comment: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "demo"},
    )

class Knowledge(QingshuModel):
    """HR · Knowledge. Fields from standard field table."""

    kb_domain: KbDomain | None = Field(
        default=None,
        description="Knowledge Domain. repair|policy|hr|product",
        json_schema_extra={"example": "repair"},
    )
    kb_doc_id: str | None = Field(
        default=None,
        description="KnowledgeDocumentID. DocumentID",
        json_schema_extra={"example": "KB-REP-0012"},
    )
    kb_chunk_id: str | None = Field(
        default=None,
        description="KnowledgeChunkID. ChunkID",
        json_schema_extra={"example": "CHK-88"},
    )
    kb_score: float | None = Field(
        default=None,
        description="search Score. searchScore",
        json_schema_extra={"example": "0.83"},
    )
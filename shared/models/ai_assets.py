"""Data models · ai_assets (from standard-field-glossary)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import StepStatus, TagDomain


class AIOutput(QingshuModel):
    """Shared AI asset · AIOutput.

    Standard fields + BLUEPRINT:`id, producer_skill, consumer_allow, payload, run_id, ts`. 
    """

    ai_output_id: str | None = Field(
        default=None,
        description="AI output id. Unique shared output identifier",
        json_schema_extra={"example": "AIO-10001"},
    )
    producer_skill: str | None = Field(
        default=None,
        description="Producer skill. Source skill_id",
        json_schema_extra={"example": "fill_ticket"},
    )
    consumer_allow: list[str] | None = Field(
        default=None,
        description="Allowed consumers. Subscribable skill list",
    )
    payload: dict[str, Any] | list[Any] | None = Field(
        default=None,
        description="Output payload. Structured output body",
    )
    payload_schema: str | None = Field(
        default=None,
        description="Payload schema. Payload structure version",
        json_schema_extra={"example": "ticket_draft_v1"},
    )
    run_id: str | None = Field(
        default=None,
        description="Run id. Agent run that produced this output",
        json_schema_extra={"example": "run_abc123"},
    )
    ts: datetime | None = Field(
        default=None,
        description="Output timestamp",
        json_schema_extra={"example": "2026-08-01T12:00:00+08:00"},
    )


class TagVocabulary(QingshuModel):
    """Shared AI asset · TagVocabulary. Shared semantic tag dictionary."""

    tag_id: str | None = Field(
        default=None,
        description="Tag id. Standard shared semantic tag id",
        json_schema_extra={"example": "TAG-short-range"},
    )
    tag_name: str | None = Field(
        default=None,
        description="Tag name. Display label",
        json_schema_extra={"example": "Short range"},
    )
    tag_domain: TagDomain | None = Field(
        default=None,
        description="Tag domain. product|service|app|channel|risk",
        json_schema_extra={"example": "product"},
    )
    tag_parent_id: str | None = Field(
        default=None,
        description="Parent tag id. Tag tree",
        json_schema_extra={"example": "TAG-ROOT-PRODUCT"},
    )
    tag_vocab_version: str | None = Field(
        default=None,
        description="Tag vocabulary version. Shared semantic version",
        json_schema_extra={"example": "voc-tags-2026.07"},
    )


class CapabilityCatalog(QingshuModel):
    """Shared AI asset · CapabilityCatalog. Capability catalog."""

    skill_id: str | None = Field(
        default=None,
        description="Skill id. Capability catalog primary key",
        json_schema_extra={"example": "repair_kb"},
    )
    skill_desc: str | None = Field(
        default=None,
        description="Skill description. Capability summary",
        json_schema_extra={"example": "Repair KB Q&A"},
    )
    input_schema: dict[str, Any] | None = Field(
        default=None,
        description="Input schema. Input contract",
    )
    output_schema: dict[str, Any] | None = Field(
        default=None,
        description="Output schema. Output contract",
    )
    allowed_tools: list[str] | None = Field(
        default=None,
        description="Allowed tools. Callable tool list",
    )


class RunLog(QingshuModel):
    """Shared AI asset · RunLog. Collaboration layer step log."""

    run_id: str | None = Field(
        default=None,
        description="RunID",
        json_schema_extra={"example": "run_abc123"},
    )
    step_name: str | None = Field(
        default=None,
        description="Step name. Control loop step",
        json_schema_extra={"example": "retrieve"},
    )
    step_status: StepStatus | None = Field(
        default=None,
        description="Step status. ok|error|skipped",
        json_schema_extra={"example": "ok"},
    )
    step_ts: datetime | None = Field(
        default=None,
        description="Step time. Step timestamp",
        json_schema_extra={"example": "2026-08-01T12:00:00+08:00"},
    )
    detail: dict[str, Any] | None = Field(
        default=None,
        description="Step detail (optional)",
    )

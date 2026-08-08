"""Data models · meta (from standard-field-glossary)."""

from __future__ import annotations

from datetime import date, datetime

from typing import Any

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import PeriodType, TrafficLight

class ReportMeta(QingshuModel):
    """Metadata · ReportMeta. Fields from standard field table."""

    report_id: str | None = Field(
        default=None,
        description="ID. unique identifier",
        json_schema_extra={"example": "CH-RPT-2026-07-EAST"},
    )
    report_type: str | None = Field(
        default=None,
        description="Report type. Report type code",
        json_schema_extra={"example": "channel_analysis"},
    )
    period: str | None = Field(
        default=None,
        description="Week. /Week/ /",
        json_schema_extra={"example": "2026-07"},
    )
    period_type: PeriodType | None = Field(
        default=None,
        description="Week Type. day|week|month|quarter|custom",
        json_schema_extra={"example": "month"},
    )
    period_start: date | None = Field(
        default=None,
        description="Week Start.",
        json_schema_extra={"example": "2026-07-01"},
    )
    period_end: date | None = Field(
        default=None,
        description="Week End. End",
        json_schema_extra={"example": "2026-07-31"},
    )
    generated_at: datetime | None = Field(
        default=None,
        description="Time. Time",
        json_schema_extra={"example": "2026-08-01T10:00:00+08:00"},
    )
    data_as_of: datetime | None = Field(
        default=None,
        description="Data.",
        json_schema_extra={"example": "2026-07-31T23:59:59+08:00"},
    )
    run_id: str | None = Field(
        default=None,
        description="RunID. Agent/ RunID",
        json_schema_extra={"example": "run_abc123"},
    )
    producer_skill: str | None = Field(
        default=None,
        description="Producer skill. skill that writes to shared layer",
        json_schema_extra={"example": "channel_analysis"},
    )
    traffic_light: TrafficLight | None = Field(
        default=None,
        description=". red|yellow|green",
        json_schema_extra={"example": "yellow"},
    )
    narrative_summary: str | None = Field(
        default=None,
        description="NLGSummary. Summary",
        json_schema_extra={"example": "East pickup 83%; color stockout top driver"},
    )
    action_suggestions: Any | None = Field(
        default=None,
        description="List. Structure",
    )
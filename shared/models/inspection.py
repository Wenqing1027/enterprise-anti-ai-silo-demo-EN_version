"""Data models · inspection (from standard-field-glossary)."""

from __future__ import annotations

from datetime import date, datetime

from typing import Any

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import PassFail

class Inspection(QingshuModel):
    """Inspection · Inspection. Fields from standard field table."""

    inspect_id: str | None = Field(
        default=None,
        description="InspectionID. Inspection ID",
        json_schema_extra={"example": "INS-20260728-014"},
    )
    inspect_time: datetime | None = Field(
        default=None,
        description="InspectionTime. InspectionTime",
        json_schema_extra={"example": "2026-07-28T08:30:00+08:00"},
    )
    check_item: str | None = Field(
        default=None,
        description=". Name",
        json_schema_extra={"example": "VI"},
    )
    ai_confidence: float | None = Field(
        default=None,
        description="AI.",
        json_schema_extra={"example": "0.91"},
    )
    pass_fail: PassFail | None = Field(
        default=None,
        description="/. pass|fail",
        json_schema_extra={"example": "fail"},
    )
    photo_url: str | None = Field(
        default=None,
        description="URL.",
        json_schema_extra={"example": "https://../store.jpg"},
    )
    morning_photo_url: str | None = Field(
        default=None,
        description="URL. Score-",
        json_schema_extra={"example": "https://../am.jpg"},
    )
    evening_photo_url: str | None = Field(
        default=None,
        description="URL. Score-",
        json_schema_extra={"example": "https://../pm.jpg"},
    )
    competitor_logo_detected: Any | None = Field(
        default=None,
        description="CompetitorLogo. CompetitorIdentifier",
    )
    suspect_type: str | None = Field(
        default=None,
        description="Type. Type",
        json_schema_extra={"example": "Non-exclusive display"},
    )
    vi_score: float | None = Field(
        default=None,
        description="VI Score. VI Score",
        json_schema_extra={"example": "78"},
    )
    rectify_ticket_id: str | None = Field(
        default=None,
        description="Ticket.",
        json_schema_extra={"example": "RC-8891"},
    )
    due_date: date | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "2026-08-05"},
    )

class Brand(QingshuModel):
    """Inspection · Brand. Fields from standard field table."""

    mention_cnt_24h: int | None = Field(
        default=None,
        description="24h. Reputation",
        json_schema_extra={"example": "1260"},
    )
    reputation_score: float | None = Field(
        default=None,
        description="Score.",
        json_schema_extra={"example": "71"},
    )
    hotspot_term: str | None = Field(
        default=None,
        description=". Reputation",
        json_schema_extra={"example": "Range"},
    )
    growth_velocity: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "3.2"},
    )
    mi_consistency_score: float | None = Field(
        default=None,
        description="MI Score. -",
        json_schema_extra={"example": "66"},
    )
    bvp_memorability: float | None = Field(
        default=None,
        description="BVP. BVP",
        json_schema_extra={"example": "0.42"},
    )
    bvp_understanding: float | None = Field(
        default=None,
        description="BVP. BVP",
        json_schema_extra={"example": "0.55"},
    )
    purchase_intent: float | None = Field(
        default=None,
        description=". BVP/",
        json_schema_extra={"example": "0.48"},
    )
    energy_kwh_per_vehicle: float | None = Field(
        default=None,
        description=". Manufacturing",
        json_schema_extra={"example": "128"},
    )
    co2e_t: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "sequester"},
    )
    scrap_battery_recycle_rate: float | None = Field(
        default=None,
        description="Battery Rate. Rate",
        json_schema_extra={"example": "91.0"},
    )
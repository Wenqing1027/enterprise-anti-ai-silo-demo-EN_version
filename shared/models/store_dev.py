"""Data models · store_dev (from standard-field-glossary)."""

from __future__ import annotations

from datetime import date

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import AdmissionSuggest, RiskLevel, SelfCoverageFlag, StoreGrade

class StoreDev(QingshuModel):
    """Channel · StoreDev. Fields from standard field table."""

    blank_l1_plan_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "18"},
    )
    blank_l1_opened_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "11"},
    )
    blank_l1_achieve_rate: float | None = Field(
        default=None,
        description="AttainmentRate. /",
        json_schema_extra={"example": "61.1"},
    )
    store_dev_plan_cnt: int | None = Field(
        default=None,
        description="Store.",
        json_schema_extra={"example": "120"},
    )
    store_dev_done_cnt: int | None = Field(
        default=None,
        description="Store.",
        json_schema_extra={"example": "74"},
    )
    store_dev_rate: float | None = Field(
        default=None,
        description="Store Rate. /",
        json_schema_extra={"example": "61.7"},
    )
    market_capacity_annual: int | None = Field(
        default=None,
        description="Domain.",
        json_schema_extra={"example": "42000"},
    )
    self_coverage_flag: SelfCoverageFlag | None = Field(
        default=None,
        description="Own-brand coverage flag. yes|weak|blank",
        json_schema_extra={"example": "blank"},
    )
    open_roi_months: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "14"},
    )
    support_quota_total_wan: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "15"},
    )
    support_quota_applied_wan: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "8"},
    )
    support_quota_remain_wan: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "7"},
    )
    first_order_qty: int | None = Field(
        default=None,
        description="Order. Pickup",
        json_schema_extra={"example": "80"},
    )
    m1_m3_order_qty: int | None = Field(
        default=None,
        description="1-3 Order. Pickup",
        json_schema_extra={"example": "210"},
    )
    gantt_owner: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "Zhang San"},
    )
    gantt_start: date | None = Field(
        default=None,
        description="Start. Start",
        json_schema_extra={"example": "2026-07-01"},
    )
    gantt_end: date | None = Field(
        default=None,
        description="End. End",
        json_schema_extra={"example": "2026-09-15"},
    )
    fitout_suggest_grade: StoreGrade | None = Field(
        default=None,
        description="Level.",
        json_schema_extra={"example": "B"},
    )

class Risk(QingshuModel):
    """Channel · Risk. Fields from standard field table."""

    credit_code: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "9132XXXXXXXX"},
    )
    reg_capital_wan: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "500"},
    )
    lawsuit_cnt_3y: int | None = Field(
        default=None,
        description="3. Risk",
        json_schema_extra={"example": "2"},
    )
    dishonest_flag: bool | None = Field(
        default=None,
        description="Whether.",
        json_schema_extra={"example": "false"},
    )
    negative_news_cnt_90d: int | None = Field(
        default=None,
        description="90 Reputation. ReputationRisk",
        json_schema_extra={"example": "1"},
    )
    risk_level: RiskLevel | None = Field(
        default=None,
        description="RiskLevel. low|medium|high",
        json_schema_extra={"example": "medium"},
    )
    risk_score: float | None = Field(
        default=None,
        description="Risk Score. RiskScore",
        json_schema_extra={"example": "62"},
    )
    admission_suggest: AdmissionSuggest | None = Field(
        default=None,
        description=". pass|supplement|reject",
        json_schema_extra={"example": "supplement"},
    )
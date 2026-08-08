"""Data models · alert (from standard-field-glossary)."""

from __future__ import annotations

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import AlertType, Severity

class Alert(QingshuModel):
    """Alert · Alert. Fields from standard field table."""

    alert_id: str | None = Field(
        default=None,
        description="AlertID. Alertunique ID",
        json_schema_extra={"example": "ALERT-20260728-014"},
    )
    alert_type: AlertType | None = Field(
        default=None,
        description="AlertType. Sales volume | | | |Competitor",
        json_schema_extra={"example": "shortage"},
    )
    metric_name: str | None = Field(
        default=None,
        description="Metric. Metric",
        json_schema_extra={"example": "mom_rate"},
    )
    metric_value: float | None = Field(
        default=None,
        description="Metric.",
        json_schema_extra={"example": "-12.4"},
    )
    threshold_value: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "-10.0"},
    )
    severity: Severity | None = Field(
        default=None,
        description=". P0|P1|P2",
        json_schema_extra={"example": "P0"},
    )
    required_action: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "Replenish color within 3 days"},
    )
    verify_method: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "Second inspection"},
    )

class Collab(QingshuModel):
    """Alert · Collab. Fields from standard field table."""

    cross_issue_cnt: int | None = Field(
        default=None,
        description="Cross-department.",
        json_schema_extra={"example": "17"},
    )
    closed_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "9"},
    )
    overdue_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "3"},
    )
    response_hours: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "26"},
    )
    pilot_vs_control_delta: float | None = Field(
        default=None,
        description=". vs Metric",
        json_schema_extra={"example": "8.5"},
    )
    resolution_id: str | None = Field(
        default=None,
        description="ID.",
        json_schema_extra={"example": "RES-2026W30-01"},
    )
    owner_dept: str | None = Field(
        default=None,
        description="department. department",
        json_schema_extra={"example": "Product innovation lab"},
    )
    verify_metric: str | None = Field(
        default=None,
        description="Metric. KPI",
        json_schema_extra={"example": "Range theme negative share"},
    )
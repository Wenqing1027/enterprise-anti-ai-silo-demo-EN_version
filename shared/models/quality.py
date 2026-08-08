"""Data models · quality (from standard-field-glossary)."""

from __future__ import annotations

from datetime import datetime

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import QcResult, RecallLevel

class Quality(QingshuModel):
    """Manufacturing · Quality. Fields from standard field table."""

    test_station: str | None = Field(
        default=None,
        description=". Quality check",
        json_schema_extra={"example": "OBD-Test bench-02"},
    )
    test_ts: datetime | None = Field(
        default=None,
        description="Time. Time",
        json_schema_extra={"example": "2026-07-28T14:22:00+08:00"},
    )
    obd_protocol: str | None = Field(
        default=None,
        description="OBD.",
        json_schema_extra={"example": "ISO15765"},
    )
    voltage_v: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "54.6"},
    )
    current_a: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "12.3"},
    )
    speed_rpm: float | None = Field(
        default=None,
        description=". Motor",
        json_schema_extra={"example": "480"},
    )
    controller_temp_c: float | None = Field(
        default=None,
        description="Controller.",
        json_schema_extra={"example": "46"},
    )
    qc_result: QcResult | None = Field(
        default=None,
        description="Quality check. pass|fail",
        json_schema_extra={"example": "pass"},
    )
    operator_id: str | None = Field(
        default=None,
        description="Staff.",
        json_schema_extra={"example": "OP-331"},
    )
    part_name: str | None = Field(
        default=None,
        description="Name.",
        json_schema_extra={"example": "Controller"},
    )
    part_batch_no: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "PB-CTRL-2026W27"},
    )
    supplier_id: str | None = Field(
        default=None,
        description="ID.",
        json_schema_extra={"example": "SUP-8821"},
    )
    delta_e: float | None = Field(
        default=None,
        description="ΔE.",
        json_schema_extra={"example": "0.8"},
    )
    gloss: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "85"},
    )
    defect_type: str | None = Field(
        default=None,
        description="DefectType. / /",
        json_schema_extra={"example": "color mismatch"},
    )
    anomaly_score: float | None = Field(
        default=None,
        description="Score. /",
        json_schema_extra={"example": "0.86"},
    )
    predict_fail_days: int | None = Field(
        default=None,
        description="Days.",
        json_schema_extra={"example": "14"},
    )
    release_ts: datetime | None = Field(
        default=None,
        description="Time. Pass",
        json_schema_extra={"example": "2026-07-28T16:00:00+08:00"},
    )
    trace_package_url: str | None = Field(
        default=None,
        description=". Data",
        json_schema_extra={"example": "s3://trace/VINxxx.zip"},
    )
    recall_level: RecallLevel | None = Field(
        default=None,
        description="Level. watch|targeted|recall_eval",
        json_schema_extra={"example": "watch"},
    )
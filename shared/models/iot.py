"""Data models · iot (from standard-field-glossary)."""

from __future__ import annotations

from pydantic import Field

from shared.models.base import QingshuModel

class Telemetry(QingshuModel):
    """IoT · Telemetry. Fields from standard field table plus relation keys."""

    vin: str | None = Field(
        default=None,
        description="VIN. Related to Vehicle",
        json_schema_extra={"example": "LQXXXX2026A0001"},
    )

    fault_code: str | None = Field(
        default=None,
        description="/Alert. Alert",
        json_schema_extra={"example": "BMS_OT_01"},
    )
    iot_alert_cnt: int | None = Field(
        default=None,
        description="AlertCount. Week AlertCount",
        json_schema_extra={"example": "3"},
    )
    mileage_km: float | None = Field(
        default=None,
        description=". /Week",
        json_schema_extra={"example": "3260"},
    )
    soc_pct: float | None = Field(
        default=None,
        description="SOC.",
        json_schema_extra={"example": "64"},
    )
    telemetry_coverage_rate: float | None = Field(
        default=None,
        description="Rate. telemetryVehicle",
        json_schema_extra={"example": "81.0"},
    )
    battery_health_pct: float | None = Field(
        default=None,
        description="BatteryHealth. SOH",
        json_schema_extra={"example": "92"},
    )
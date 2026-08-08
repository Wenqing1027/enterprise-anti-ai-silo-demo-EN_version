"""Data models · vehicle (from standard-field-glossary)."""

from __future__ import annotations

from datetime import date

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import BatteryType

class Vehicle(QingshuModel):
    """Vehicle · Vehicle. Fields from standard field table."""

    vin: str | None = Field(
        default=None,
        description="VIN. Unique",
        json_schema_extra={"example": "LQXXXX2026A0001"},
    )
    frame_no: str | None = Field(
        default=None,
        description=". PDABinding",
        json_schema_extra={"example": "FR-778812"},
    )
    sn: str | None = Field(
        default=None,
        description=". Production line",
        json_schema_extra={"example": "SN-202607-8891"},
    )
    vehicle_model: str | None = Field(
        default=None,
        description=". /",
        json_schema_extra={"example": "E60"},
    )
    vehicle_config: str | None = Field(
        default=None,
        description="Type. Tier",
        json_schema_extra={"example": "lithium flagship"},
    )
    color: str | None = Field(
        default=None,
        description="Color. Color",
        json_schema_extra={"example": "matte black"},
    )
    battery_type: BatteryType | None = Field(
        default=None,
        description="BatteryType. lead_acid|lithium|graphene",
        json_schema_extra={"example": "lithium"},
    )
    battery_spec: str | None = Field(
        default=None,
        description="Battery.",
        json_schema_extra={"example": "48V24Ah"},
    )
    claimed_range_km: float | None = Field(
        default=None,
        description="Range. Range",
        json_schema_extra={"example": "80"},
    )
    purchase_date: date | None = Field(
        default=None,
        description="Date. User",
        json_schema_extra={"example": "2025-08-01"},
    )
    purchase_year: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "2025"},
    )
    is_smart_vehicle: bool | None = Field(
        default=None,
        description="WhetherSmart. Whether 4G/",
        json_schema_extra={"example": "true"},
    )
    plant: str | None = Field(
        default=None,
        description="Producer. Manufacturing",
        json_schema_extra={"example": "East Plant 1"},
    )
    line_id: str | None = Field(
        default=None,
        description="Production lineID. Production line",
        json_schema_extra={"example": "LINE-03"},
    )
    batch_no: str | None = Field(
        default=None,
        description="Producer.",
        json_schema_extra={"example": "BATCH-2026W28-E60"},
    )
    ota_version: str | None = Field(
        default=None,
        description="OTAVersion. Version",
        json_schema_extra={"example": "v2.3.1"},
    )
    customer_id: str | None = Field(
        default=None,
        description="Customer ID. Related to Customer",
        json_schema_extra={"example": "CUS-10086"},
    )
    store_id: str | None = Field(
        default=None,
        description="Store ID. / Store(optional)",
        json_schema_extra={"example": "ST-8891"},
    )
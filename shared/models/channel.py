"""Data models · channel (from standard-field-glossary)."""

from __future__ import annotations

from datetime import date

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import StoreGrade, StoreType

class Dealer(QingshuModel):
    """Channel Data · Dealer. Fields from standard field table."""

    dealer_id: str | None = Field(
        default=None,
        description="/Dealer ID. Dealerunique ID",
        json_schema_extra={"example": "DLR-3201"},
    )
    dealer_name: str | None = Field(
        default=None,
        description="DealerName. Dealer",
        json_schema_extra={"example": "Qingshu Nanjing Jiangning tier-1"},
    )
    legal_person: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "Wang XX"},
    )
    open_account_date: date | None = Field(
        default=None,
        description="Time. Dealer",
        json_schema_extra={"example": "2024-03-12"},
    )
    developer_name: str | None = Field(
        default=None,
        description=". Channel",
        json_schema_extra={"example": "Li Dev"},
    )

class Store(QingshuModel):
    """Channel Data · Store. Fields from standard field table."""

    store_id: str | None = Field(
        default=None,
        description="Store ID. Storeunique ID",
        json_schema_extra={"example": "ST-8891"},
    )
    store_name: str | None = Field(
        default=None,
        description="StoreName. Store",
        json_schema_extra={"example": "Qingshu Nanjing Jiangning store"},
    )
    store_address: str | None = Field(
        default=None,
        description="Store.",
        json_schema_extra={"example": "XX 88"},
    )
    store_type: StoreType | None = Field(
        default=None,
        description="StoreType. exclusive|mixed|non_exclusive",
        json_schema_extra={"example": "exclusive"},
    )
    store_grade: StoreGrade | None = Field(
        default=None,
        description="StoreLevel. A|B|C|D",
        json_schema_extra={"example": "A"},
    )
    store_area_sqm: float | None = Field(
        default=None,
        description="Store.",
        json_schema_extra={"example": "120"},
    )
    biz_district: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "demo"},
    )

class Guide(QingshuModel):
    """Channel Data · Guide. Fields from standard field table."""

    guide_id: str | None = Field(
        default=None,
        description="ID. ID",
        json_schema_extra={"example": "GD-1022"},
    )
    channel_account_id: str | None = Field(
        default=None,
        description="ID. /",
        json_schema_extra={"example": "DY-991"},
    )
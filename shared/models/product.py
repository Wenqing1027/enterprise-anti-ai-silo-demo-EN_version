"""Data models · product (from standard-field-glossary)."""

from __future__ import annotations

from datetime import date

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import HotSlowFlag

class SKU(QingshuModel):
    """SKUSKU · SKU. Fields from standard field table."""

    sku_id: str | None = Field(
        default=None,
        description="SKU ID. SKUunique ID",
        json_schema_extra={"example": "SKU-E60-BK"},
    )
    sku_name: str | None = Field(
        default=None,
        description="SKUName. SKUDisplay name",
        json_schema_extra={"example": "E60"},
    )
    asp_cny: float | None = Field(
        default=None,
        description="ASP.",
        json_schema_extra={"example": "3299"},
    )
    hot_slow_flag: HotSlowFlag | None = Field(
        default=None,
        description=". hot|normal|slow",
        json_schema_extra={"example": "hot"},
    )
    substitute_sku_id: str | None = Field(
        default=None,
        description="SKU. Stockout",
        json_schema_extra={"example": "SKU-E60-GY"},
    )

class Competitor(QingshuModel):
    """SKUSKU · Competitor. Fields from standard field table."""

    competitor_brand: str | None = Field(
        default=None,
        description="Competitor. Competitor",
        json_schema_extra={"example": "Yadea"},
    )
    competitor_model: str | None = Field(
        default=None,
        description="Competitor. Competitor",
        json_schema_extra={"example": "XX"},
    )
    competitor_price_cny: float | None = Field(
        default=None,
        description="Competitor. Competitor /Campaign",
        json_schema_extra={"example": "3699"},
    )
    competitor_share: float | None = Field(
        default=None,
        description="CompetitorRegion. Region",
        json_schema_extra={"example": "28.0"},
    )
    competitor_share_pp_change: float | None = Field(
        default=None,
        description="Score.",
        json_schema_extra={"example": "-1.2"},
    )
    promo_type: str | None = Field(
        default=None,
        description="Type. CampaignType",
        json_schema_extra={"example": "trade-in"},
    )
    promo_region: str | None = Field(
        default=None,
        description="Region. CampaignRegion",
        json_schema_extra={"example": "Jiangsu-Anhui"},
    )
    promo_window: str | None = Field(
        default=None,
        description=". CampaignTime",
        json_schema_extra={"example": "2026-07-01~07-31"},
    )
    price_cut_amt: float | None = Field(
        default=None,
        description="Amount.",
        json_schema_extra={"example": "300"},
    )
    sentiment_score: float | None = Field(
        default=None,
        description="Score. Competitor",
        json_schema_extra={"example": "0.62"},
    )
    launch_date: date | None = Field(
        default=None,
        description="Date. Competitor",
        json_schema_extra={"example": "2026-06-18"},
    )
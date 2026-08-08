"""Data models · retail (from standard-field-glossary)."""

from __future__ import annotations

from pydantic import Field

from shared.models.base import QingshuModel

class Retail(QingshuModel):
    """RetailMarketing · Retail. Fields from standard field table."""

    retail_qty: int | None = Field(
        default=None,
        description="Retail. /Retail",
        json_schema_extra={"example": "46"},
    )
    retail_qty_day: int | None = Field(
        default=None,
        description="Retail. Retail",
        json_schema_extra={"example": "6"},
    )
    retail_qty_mtd: int | None = Field(
        default=None,
        description="Retail. Retail",
        json_schema_extra={"example": "142"},
    )
    retail_yoy: float | None = Field(
        default=None,
        description="Retail. Retail",
        json_schema_extra={"example": "8.2"},
    )
    writeoff_qty: int | None = Field(
        default=None,
        description="Quantity. Campaign",
        json_schema_extra={"example": "28"},
    )
    redeem_rate: float | None = Field(
        default=None,
        description="Rate. /",
        json_schema_extra={"example": "62.0"},
    )
    gross_margin_amt: float | None = Field(
        default=None,
        description=". Amount",
        json_schema_extra={"example": "9860"},
    )
    gross_margin_rate: float | None = Field(
        default=None,
        description="Rate. Rate",
        json_schema_extra={"example": "17.9"},
    )
    non_exclusive_rate: float | None = Field(
        default=None,
        description="Non-exclusive displayRate. /Non-exclusive display",
        json_schema_extra={"example": "0"},
    )
    non_exclusive_flag: bool | None = Field(
        default=None,
        description="Non-exclusive display. WhetherNon-exclusive displayStore",
        json_schema_extra={"example": "false"},
    )

class Campaign(QingshuModel):
    """RetailMarketing · Campaign. Fields from standard field table."""

    campaign_id: str | None = Field(
        default=None,
        description="CampaignID. MarketingCampaignID",
        json_schema_extra={"example": "CAMP-summer-trade-in"},
    )
    campaign_name: str | None = Field(
        default=None,
        description="CampaignName. Campaign",
        json_schema_extra={"example": "Summer trade-in"},
    )
    campaign_goal: str | None = Field(
        default=None,
        description="CampaignTarget. CampaignTarget",
        json_schema_extra={"example": "Improve renewal conversion"},
    )
    campaign_budget: float | None = Field(
        default=None,
        description="Campaign.",
        json_schema_extra={"example": "50000"},
    )
    participants: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "3200"},
    )
    campaign_roi: float | None = Field(
        default=None,
        description="CampaignROI. Output",
        json_schema_extra={"example": "2.4"},
    )
    campaign_complaint_rate: float | None = Field(
        default=None,
        description="CampaignComplaintRate. Campaign ComplaintRate",
        json_schema_extra={"example": "0.3"},
    )

class Content(QingshuModel):
    """RetailMarketing · Content. Fields from standard field table."""

    short_video_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "2140"},
    )
    short_video_valid_participate_rate: float | None = Field(
        default=None,
        description="Rate.",
        json_schema_extra={"example": "38.5"},
    )
    followers: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "12400"},
    )
    play_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "86000"},
    )
    gmv_convert_rate: float | None = Field(
        default=None,
        description="Rate. →",
        json_schema_extra={"example": "1.8"},
    )
    deals_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "36"},
    )
    gmv: float | None = Field(
        default=None,
        description="GMV.",
        json_schema_extra={"example": "118764"},
    )
    aov: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "3299"},
    )
    valid_seller_flag: bool | None = Field(
        default=None,
        description="Whether.",
        json_schema_extra={"example": "true"},
    )
    live_sessions: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "12"},
    )
    live_watch_uv: int | None = Field(
        default=None,
        description="UV.",
        json_schema_extra={"example": "5600"},
    )
    influencer_cvr: float | None = Field(
        default=None,
        description="Rate.",
        json_schema_extra={"example": "2.1"},
    )
    refund_rate: float | None = Field(
        default=None,
        description="Rate.",
        json_schema_extra={"example": "1.2"},
    )
    content_script_id: str | None = Field(
        default=None,
        description="/ ID. Content ID",
        json_schema_extra={"example": "SCRIPT-range-compare-01"},
    )
    benchmark_case_id: str | None = Field(
        default=None,
        description="ID.",
        json_schema_extra={"example": "CASE-suzhou-wuzhong-store"},
    )

class Outreach(QingshuModel):
    """RetailMarketing · Outreach. Fields from standard field table."""

    channel_quota_daily: int | None = Field(
        default=None,
        description="Channel. Outreach",
        json_schema_extra={"example": "5000"},
    )
    delivery_rate: float | None = Field(
        default=None,
        description="Rate. Rate",
        json_schema_extra={"example": "96.2"},
    )
    open_rate: float | None = Field(
        default=None,
        description="Rate. / Rate",
        json_schema_extra={"example": "28.4"},
    )
    connect_rate: float | None = Field(
        default=None,
        description="Rate. Outbound call Rate",
        json_schema_extra={"example": "41.0"},
    )
    transfer_human_cnt: int | None = Field(
        default=None,
        description=". Intent",
        json_schema_extra={"example": "86"},
    )
    template_approve_days: float | None = Field(
        default=None,
        description="Week. Days",
        json_schema_extra={"example": "2"},
    )
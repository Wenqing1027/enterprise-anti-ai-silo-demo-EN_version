"""Data models · activation (from standard-field-glossary)."""

from __future__ import annotations

from pydantic import Field

from shared.models.base import QingshuModel

class Activation(QingshuModel):
    """App · Activation. Fields from standard field table."""

    cum_sales_units: int | None = Field(
        default=None,
        description="Sales volume. Sales volume",
        json_schema_extra={"example": "2500000"},
    )
    active_owners_est: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "1800000"},
    )
    app_register_cnt: int | None = Field(
        default=None,
        description="App. User",
        json_schema_extra={"example": "920000"},
    )
    bind_vehicle_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "610000"},
    )
    mau: int | None = Field(
        default=None,
        description="MAU. Active",
        json_schema_extra={"example": "210000"},
    )
    dau: int | None = Field(
        default=None,
        description="DAU. Active",
        json_schema_extra={"example": "42000"},
    )
    activation_rate: float | None = Field(
        default=None,
        description="Rate. /",
        json_schema_extra={"example": "33.9"},
    )
    funnel_step: str | None = Field(
        default=None,
        description="Step. → → → →",
        json_schema_extra={"example": "bind vehicle"},
    )
    funnel_uv: int | None = Field(
        default=None,
        description="StepUV. Step User",
        json_schema_extra={"example": "88000"},
    )
    funnel_cvr: float | None = Field(
        default=None,
        description="Step Rate.",
        json_schema_extra={"example": "62.0"},
    )
    tab_name: str | None = Field(
        default=None,
        description="App Tab. featureTab",
        json_schema_extra={"example": "use vehicle"},
    )
    pv: int | None = Field(
        default=None,
        description="PV.",
        json_schema_extra={"example": "560000"},
    )
    uv: int | None = Field(
        default=None,
        description="UV.",
        json_schema_extra={"example": "120000"},
    )
    stay_seconds: float | None = Field(
        default=None,
        description=". Duration",
        json_schema_extra={"example": "46"},
    )
    push_click_rate: float | None = Field(
        default=None,
        description="Push Rate. Push CTR",
        json_schema_extra={"example": "8.6"},
    )
    faq_cnt: int | None = Field(
        default=None,
        description="FAQ. Knowledge",
        json_schema_extra={"example": "320"},
    )
    top20_ticket_coverage_rate: float | None = Field(
        default=None,
        description="Top20Ticket Rate. FAQ Ticket",
        json_schema_extra={"example": "71.0"},
    )
    oneid_coverage_rate: float | None = Field(
        default=None,
        description="OneID Rate. User",
        json_schema_extra={"example": "64.0"},
    )
    orphan_user_cnt: int | None = Field(
        default=None,
        description="User. User",
        json_schema_extra={"example": "120000"},
    )
    koc_score: float | None = Field(
        default=None,
        description="KOCScore. KOC Score",
        json_schema_extra={"example": "81"},
    )
    post_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "24"},
    )
    interact_rate: float | None = Field(
        default=None,
        description="Rate. /",
        json_schema_extra={"example": "6.8"},
    )

class O2O(QingshuModel):
    """App · O2O. Fields from standard field table."""

    platform_order_cnt: int | None = Field(
        default=None,
        description="Order. Order",
        json_schema_extra={"example": "1500"},
    )
    lead_phone_cnt: int | None = Field(
        default=None,
        description="Phone number.",
        json_schema_extra={"example": "980"},
    )
    store_redeem_cnt: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "420"},
    )
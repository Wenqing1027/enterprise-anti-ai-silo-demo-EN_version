"""Data models · customer (from standard-field-glossary)."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import IdentityType, IntentLevel, OneIdMatchMethod, OutreachChannel, PaidType, RenewPoolLayer, RfmSegment

class Customer(QingshuModel):
    """Customer · Customer. Fields from standard field table."""

    customer_id: str | None = Field(
        default=None,
        description="Customer ID. Unified customer master data ID",
        json_schema_extra={"example": "CUS-10086"},
    )
    phone_masked: str | None = Field(
        default=None,
        description="Phone (masked). Masked phone number",
        json_schema_extra={"example": "138****5678"},
    )
    openid: str | None = Field(
        default=None,
        description="OpenID. WeChat OpenID",
        json_schema_extra={"example": "oxxx"},
    )
    unionid: str | None = Field(
        default=None,
        description="UnionID. WeChat UnionID",
        json_schema_extra={"example": "uxxx"},
    )
    identity_type: IdentityType | None = Field(
        default=None,
        description="Identity type. end_user|dealer|prospect|employee",
        json_schema_extra={"example": "end_user"},
    )
    oneid: str | None = Field(
        default=None,
        description="OneID. Cross-system unified identity",
        json_schema_extra={"example": "OID-9f3a"},
    )
    oneid_match_method: OneIdMatchMethod | None = Field(
        default=None,
        description="Identity match method. phone|device|vin|probabilistic",
        json_schema_extra={"example": "phone"},
    )

class UserBehavior(QingshuModel):
    """Customer · UserBehavior. Fields from standard field table plus relation keys."""

    customer_id: str | None = Field(
        default=None,
        description="Customer ID. Related to Customer",
        json_schema_extra={"example": "CUS-10086"},
    )
    vin: str | None = Field(
        default=None,
        description="Bound vehicle VIN (optional)",
        json_schema_extra={"example": "LQXXXX2026A0001"},
    )
    app_register_flag: bool | None = Field(
        default=None,
        description="App registered. Whether registered in App",
        json_schema_extra={"example": "true"},
    )
    bind_vehicle_flag: bool | None = Field(
        default=None,
        description="Vehicle bound. Whether vehicle binding completed",
        json_schema_extra={"example": "true"},
    )
    last_active_at: datetime | None = Field(
        default=None,
        description="Last active time. Last active on App/IoT",
        json_schema_extra={"example": "2026-07-20T21:00:00+08:00"},
    )
    active_days_30d: int | None = Field(
        default=None,
        description="Active days in last 30. Active days in last 30",
        json_schema_extra={"example": "12"},
    )
    mau_flag: bool | None = Field(
        default=None,
        description="Counts toward MAU. Monthly active flag",
        json_schema_extra={"example": "true"},
    )
    dau_flag: bool | None = Field(
        default=None,
        description="Counts toward DAU. Daily active flag",
        json_schema_extra={"example": "false"},
    )
    rfm_segment: RfmSegment | None = Field(
        default=None,
        description="RFM segment. high_value|potential|silent|churn_risk",
        json_schema_extra={"example": "high_value"},
    )
    r_days: int | None = Field(
        default=None,
        description="R value (days since last active). Recency",
        json_schema_extra={"example": "18"},
    )
    f_month: int | None = Field(
        default=None,
        description="F value (monthly interactions). Frequency",
        json_schema_extra={"example": "7"},
    )
    m_value: float | None = Field(
        default=None,
        description="M value (value contribution). Parts/service spend etc.",
        json_schema_extra={"example": "860"},
    )
    first_touch_channel: str | None = Field(
        default=None,
        description="First outreach channel. First touch channel",
        json_schema_extra={"example": "400"},
    )
    last_touch_channel: str | None = Field(
        default=None,
        description="Last outreach channel. Last touch channel",
        json_schema_extra={"example": "App"},
    )

class Renewal(QingshuModel):
    """Customer · Renewal. Fields from standard field table plus relation keys."""

    customer_id: str | None = Field(
        default=None,
        description="Customer ID. Related to Customer",
        json_schema_extra={"example": "CUS-10086"},
    )
    vin: str | None = Field(
        default=None,
        description="Vehicle VIN. Related to Vehicle",
        json_schema_extra={"example": "LQXXXX2026A0001"},
    )
    service_expire_date: date | None = Field(
        default=None,
        description="Connected service expiry date. smart-vehicle service expiry",
        json_schema_extra={"example": "2026-08-15"},
    )
    due_renew_flag: bool | None = Field(
        default=None,
        description="Whether due for renewal pool. enters renewal pool",
        json_schema_extra={"example": "true"},
    )
    paid_flag: bool | None = Field(
        default=None,
        description="Whether paid. Whether payment occurred(distinguish new purchase vs renewal)",
        json_schema_extra={"example": "false"},
    )
    paid_type: PaidType | None = Field(
        default=None,
        description="Type. new_purchase|renew|unknown",
        json_schema_extra={"example": "renew"},
    )
    active_t30_flag: bool | None = Field(
        default=None,
        description="Active within 30 days before expiry. T-30Active",
        json_schema_extra={"example": "true"},
    )
    active_t7_flag: bool | None = Field(
        default=None,
        description="Active within 7 days before expiry. T-7Active",
        json_schema_extra={"example": "false"},
    )
    sleep_90d_app_flag: bool | None = Field(
        default=None,
        description="App dormant in last 90 days. no app use in 90 days",
        json_schema_extra={"example": "true"},
    )
    active_90d_4g_flag: bool | None = Field(
        default=None,
        description="4G active in last 90 days. connected vehicle active in 90 days",
        json_schema_extra={"example": "true"},
    )
    renew_intent_score: float | None = Field(
        default=None,
        description="Renewal intent score. model/rule intent score",
        json_schema_extra={"example": "0.78"},
    )
    renew_pool_layer: RenewPoolLayer | None = Field(
        default=None,
        description="RenewalPoolLayer. T-30|T-7|sleep|non_smart",
        json_schema_extra={"example": "T-30"},
    )
    outreach_channel: OutreachChannel | None = Field(
        default=None,
        description="OutreachChannel. push|sms|ai_call|human|wecom",
        json_schema_extra={"example": "ai_call"},
    )
    intent_level: IntentLevel | None = Field(
        default=None,
        description="Outbound callIntentLevel. high|mid|low",
        json_schema_extra={"example": "high"},
    )
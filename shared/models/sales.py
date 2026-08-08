"""Data models · sales (from standard-field-glossary)."""

from __future__ import annotations

from pydantic import Field

from shared.models.base import QingshuModel

class SalesMetric(QingshuModel):
    """Target · SalesMetric. Fields from standard field table."""

    sales_qty: int | None = Field(
        default=None,
        description="Pickup/Sales volume. Pickup Sales volume",
        json_schema_extra={"example": "12480"},
    )
    sales_target_qty: int | None = Field(
        default=None,
        description="Sales volumeTarget. Sales volumeTarget",
        json_schema_extra={"example": "15000"},
    )
    sales_achieve_rate: float | None = Field(
        default=None,
        description="Sales volumeAttainmentRate. Sales volume/Target",
        json_schema_extra={"example": "83.2"},
    )
    contract_qty: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "11200"},
    )
    contract_target_qty: int | None = Field(
        default=None,
        description="Target. Target",
        json_schema_extra={"example": "13000"},
    )
    contract_achieve_rate: float | None = Field(
        default=None,
        description="AttainmentRate. /Target",
        json_schema_extra={"example": "86.2"},
    )
    yoy_sales_qty: int | None = Field(
        default=None,
        description="Sales volume. Sales volume",
        json_schema_extra={"example": "10900"},
    )
    yoy_rate: float | None = Field(
        default=None,
        description="Rate.",
        json_schema_extra={"example": "14.5"},
    )
    mom_sales_qty: int | None = Field(
        default=None,
        description="Sales volume.",
        json_schema_extra={"example": "13100"},
    )
    mom_rate: float | None = Field(
        default=None,
        description="Rate.",
        json_schema_extra={"example": "-4.7"},
    )
    rank_warzone: int | None = Field(
        default=None,
        description="War zone. War zone",
        json_schema_extra={"example": "2"},
    )
    rank_subzone: int | None = Field(
        default=None,
        description="War zone. War zone",
        json_schema_extra={"example": "5"},
    )
    rank_dealer: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "18"},
    )
    full_achieve_outlet_cnt: int | None = Field(
        default=None,
        description="100%Attainment. Score",
        json_schema_extra={"example": "86"},
    )
    full_achieve_outlet_ratio: float | None = Field(
        default=None,
        description="100%Attainment. Score",
        json_schema_extra={"example": "41.3"},
    )
    abnormal_outlet_cnt: int | None = Field(
        default=None,
        description=". Quantity",
        json_schema_extra={"example": "23"},
    )
    abnormal_outlet_ratio: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "11.1"},
    )
    abnormal_reason: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "ColorStockout"},
    )
    abnormal_reason_cnt: int | None = Field(
        default=None,
        description="Count. this Count",
        json_schema_extra={"example": "9"},
    )
    core_market_gap_to_top3: int | None = Field(
        default=None,
        description=". Region",
        json_schema_extra={"example": "1260"},
    )
    online_sales_qty: int | None = Field(
        default=None,
        description="Sales volume. / Sales volume",
        json_schema_extra={"example": "860"},
    )

class Health(QingshuModel):
    """Target · Health. Fields from standard field table."""

    health_index: float | None = Field(
        default=None,
        description="OperationsHealth. HealthScore",
        json_schema_extra={"example": "72"},
    )
    sales_score: float | None = Field(
        default=None,
        description="Sales volumeScore Score. Health Score",
        json_schema_extra={"example": "75"},
    )
    retail_score: float | None = Field(
        default=None,
        description="RetailScore Score. Health Score",
        json_schema_extra={"example": "68"},
    )
    compliance_score: float | None = Field(
        default=None,
        description="Score Score. Health Score",
        json_schema_extra={"example": "80"},
    )
    complaint_score: float | None = Field(
        default=None,
        description="Score Score. Health Score",
        json_schema_extra={"example": "70"},
    )
    inventory_turn_score: float | None = Field(
        default=None,
        description="InventoryWeek Score Score. Health Score",
        json_schema_extra={"example": "65"},
    )
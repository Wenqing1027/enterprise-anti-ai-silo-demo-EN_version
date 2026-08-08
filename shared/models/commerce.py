"""Data models · commerce (from standard-field-glossary)."""

from __future__ import annotations

from datetime import date

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import AuditResult, OrderStatus, PayStatus, ShortageRootCause

class Order(QingshuModel):
    """OrderInventoryPolicy · Order. Fields from standard field table plus relation keys."""

    order_id: str | None = Field(
        default=None,
        description="Order. OrderUnique",
        json_schema_extra={"example": "SO-77821"},
    )
    dealer_id: str | None = Field(
        default=None,
        description="Dealer ID. Related to Dealer",
        json_schema_extra={"example": "DLR-3201"},
    )
    store_id: str | None = Field(
        default=None,
        description="Store ID. Related to Store",
        json_schema_extra={"example": "ST-8891"},
    )
    sku_id: str | None = Field(
        default=None,
        description="SKU ID. Related to SKU",
        json_schema_extra={"example": "SKU-E60-BK"},
    )
    customer_id: str | None = Field(
        default=None,
        description="Customer ID. Related to Customer（ C Order）",
        json_schema_extra={"example": "CUS-10086"},
    )
    order_qty: int | None = Field(
        default=None,
        description="OrderQuantity.",
        json_schema_extra={"example": "30"},
    )
    order_status: OrderStatus | None = Field(
        default=None,
        description="OrderStatus. / / / / /",
        json_schema_extra={"example": "pending_audit"},
    )
    audit_result: AuditResult | None = Field(
        default=None,
        description=". |Stockout |",
        json_schema_extra={"example": "suggest_substitute"},
    )
    policy_version: str | None = Field(
        default=None,
        description="PolicyVersion. Policy",
        json_schema_extra={"example": "2026Q3-PickupRebate-V3"},
    )

class Inventory(QingshuModel):
    """OrderInventoryPolicy · Inventory. Fields from standard field table plus relation keys."""

    sku_id: str | None = Field(
        default=None,
        description="SKU ID. Related to SKU",
        json_schema_extra={"example": "SKU-E60-BK"},
    )
    store_id: str | None = Field(
        default=None,
        description="Store ID. StoreInventory (optional)",
        json_schema_extra={"example": "ST-8891"},
    )
    dealer_id: str | None = Field(
        default=None,
        description="Dealer ID. Inventory (optional)",
        json_schema_extra={"example": "DLR-3201"},
    )
    wms_stock_qty: int | None = Field(
        default=None,
        description="WMSInventory. Inventory",
        json_schema_extra={"example": "120"},
    )
    wms_in_transit_qty: int | None = Field(
        default=None,
        description="WMS. Quantity",
        json_schema_extra={"example": "45"},
    )
    store_stock_qty: int | None = Field(
        default=None,
        description="StoreInventory. Store",
        json_schema_extra={"example": "8"},
    )
    stock_days_cover: float | None = Field(
        default=None,
        description="Inventory Days. Inventory Days",
        json_schema_extra={"example": "1.2"},
    )
    stock_age_days: int | None = Field(
        default=None,
        description="Days.",
        json_schema_extra={"example": "51"},
    )
    inventory_turn_days: float | None = Field(
        default=None,
        description="InventoryWeek Days. Week Days",
        json_schema_extra={"example": "28"},
    )
    shortage_days: int | None = Field(
        default=None,
        description="Days. StockoutDays",
        json_schema_extra={"example": "11"},
    )
    demand_daily_est: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "18"},
    )
    lost_units_est: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "198"},
    )
    lost_gmv_est: float | None = Field(
        default=None,
        description="GMV.",
        json_schema_extra={"example": "653202"},
    )
    lost_margin_est: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "117576"},
    )
    shortage_root_cause: ShortageRootCause | None = Field(
        default=None,
        description=". Production plan| |Color |",
        json_schema_extra={"example": "color_plan"},
    )
    replenish_qty_suggest: int | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "200"},
    )
    eta_date: date | None = Field(
        default=None,
        description=". ETA",
        json_schema_extra={"example": "2026-08-05"},
    )

class Policy(QingshuModel):
    """OrderInventoryPolicy · Policy. Fields from standard field table."""

    policy_version: str | None = Field(
        default=None,
        description="PolicyVersion. PolicyVersion",
        json_schema_extra={"example": "2026Q3-PickupRebate-V3"},
    )
    current_rebate_tier: str | None = Field(
        default=None,
        description="RebateTier. Tier",
        json_schema_extra={"example": "SilverTier"},
    )
    current_pickup_qty_mtd: int | None = Field(
        default=None,
        description="Pickup. Pickup",
        json_schema_extra={"example": "612"},
    )
    qty_to_next_tier: int | None = Field(
        default=None,
        description="Tier. Tier",
        json_schema_extra={"example": "188"},
    )
    next_tier_name: str | None = Field(
        default=None,
        description="Tier. TargetTier",
        json_schema_extra={"example": "GoldTier"},
    )
    next_tier_rebate_amt: float | None = Field(
        default=None,
        description="Tier Rebate. TierRebate",
        json_schema_extra={"example": "28000"},
    )
    rebate_rate: float | None = Field(
        default=None,
        description="Rebate. RebateRatio",
        json_schema_extra={"example": "3.5"},
    )
    color_bonus_amt: float | None = Field(
        default=None,
        description="Color. Color",
        json_schema_extra={"example": "2000"},
    )
    clawback_amt: float | None = Field(
        default=None,
        description="Amount. /",
        json_schema_extra={"example": "500"},
    )
    payable_amt: float | None = Field(
        default=None,
        description="Amount. Rebate",
        json_schema_extra={"example": "29500"},
    )
    settlement_id: str | None = Field(
        default=None,
        description=". ID",
        json_schema_extra={"example": "STL-2026Q3-3201"},
    )
    pay_status: PayStatus | None = Field(
        default=None,
        description="Status. unpaid|paid|exception",
        json_schema_extra={"example": "unpaid"},
    )

class ColorPlan(QingshuModel):
    """OrderInventoryPolicy · ColorPlan. Fields from standard field table."""

    color_plan_week: str | None = Field(
        default=None,
        description="ColorProduction planWeek. Production planWeek",
        json_schema_extra={"example": "2026-W31"},
    )
    color_plan_qty: int | None = Field(
        default=None,
        description="Color. thisColor",
        json_schema_extra={"example": "120"},
    )
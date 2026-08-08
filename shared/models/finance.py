"""Data models · finance (from standard-field-glossary)."""

from __future__ import annotations

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import MatchStatus

class Finance(QingshuModel):
    """· Finance. Fields from standard field table."""

    expense_id: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "EXP-202607-118"},
    )
    invoice_no: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "INV-8891200"},
    )
    po_no: str | None = Field(
        default=None,
        description="ProcurementOrder. PO",
        json_schema_extra={"example": "PO-55201"},
    )
    receipt_amt: float | None = Field(
        default=None,
        description="Amount.",
        json_schema_extra={"example": "1280.00"},
    )
    invoice_amt: float | None = Field(
        default=None,
        description="Amount.",
        json_schema_extra={"example": "1280.00"},
    )
    po_amt: float | None = Field(
        default=None,
        description="POAmount. ProcurementOrderAmount",
        json_schema_extra={"example": "1300.00"},
    )
    match_status: MatchStatus | None = Field(
        default=None,
        description="Status. match|mismatch",
        json_schema_extra={"example": "mismatch"},
    )
    diff_amt: float | None = Field(
        default=None,
        description="Amount.",
        json_schema_extra={"example": "20.00"},
    )
    diff_reason: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "demo"},
    )
    revenue_forecast: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "1.2e8"},
    )
    pickup_forecast_units: int | None = Field(
        default=None,
        description="Pickup. Pickup",
        json_schema_extra={"example": "52000"},
    )
    rebate_cashout_forecast: float | None = Field(
        default=None,
        description="Rebate. Rebate",
        json_schema_extra={"example": "8.5e6"},
    )
    opex_forecast: float | None = Field(
        default=None,
        description=". OPEX",
        json_schema_extra={"example": "2.1e7"},
    )
    net_cash_forecast: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "1.5e7"},
    )
    forecast_confidence_low: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "1.1e7"},
    )
    forecast_confidence_high: float | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "1.9e7"},
    )
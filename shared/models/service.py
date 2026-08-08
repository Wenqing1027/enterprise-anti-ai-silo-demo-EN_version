"""Data models · service (from standard-field-glossary)."""

from __future__ import annotations

from datetime import datetime

from typing import Any

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import ClueConfidence, CoverDim, FaultCategory, ModuleName, Sentiment, SopPassFail, TagDomain, TicketStatus, TicketType

class Ticket(QingshuModel):
    """Service · Ticket. Fields from standard field table plus relation keys."""

    ticket_id: str | None = Field(
        default=None,
        description="Ticket ID. Ticketunique ID",
        json_schema_extra={"example": "TK-20260728-8891"},
    )
    customer_id: str | None = Field(
        default=None,
        description="Customer ID. Related to Customer",
        json_schema_extra={"example": "CUS-10086"},
    )
    vin: str | None = Field(
        default=None,
        description="VIN. Related to Vehicle",
        json_schema_extra={"example": "LQXXXX2026A0001"},
    )
    store_id: str | None = Field(
        default=None,
        description="Store ID. Related to Store(optional)",
        json_schema_extra={"example": "ST-8891"},
    )
    dealer_id: str | None = Field(
        default=None,
        description="Dealer ID. Related to Dealer(optional)",
        json_schema_extra={"example": "DLR-3201"},
    )
    tag_id: str | None = Field(
        default=None,
        description="TagID. Related to TagVocabulary",
        json_schema_extra={"example": "TAG-short-range"},
    )
    sentiment: Sentiment | None = Field(
        default=None,
        description="Sentiment.",
        json_schema_extra={"example": "neg"},
    )
    ticket_type: TicketType | None = Field(
        default=None,
        description="TicketType. fault|consult|complaint|other",
        json_schema_extra={"example": "fault"},
    )
    fault_category: FaultCategory | None = Field(
        default=None,
        description=". Battery|Motor|Brake|Controller|Charging|Dashboard| | | |",
        json_schema_extra={"example": "battery"},
    )
    consult_category: str | None = Field(
        default=None,
        description=". Score",
        json_schema_extra={"example": "vehicle info"},
    )
    ticket_channel: str | None = Field(
        default=None,
        description="TicketChannel. 400|App| |Store",
        json_schema_extra={"example": "400"},
    )
    ticket_status: TicketStatus | None = Field(
        default=None,
        description="TicketStatus. open|processing|closed",
        json_schema_extra={"example": "open"},
    )
    ticket_created_at: datetime | None = Field(
        default=None,
        description="TicketCreated at. Created at",
        json_schema_extra={"example": "2026-07-28T09:12:00+08:00"},
    )
    handle_duration_min: float | None = Field(
        default=None,
        description="Duration.",
        json_schema_extra={"example": "18"},
    )
    is_complaint: bool | None = Field(
        default=None,
        description="WhetherComplaint. Complaint",
        json_schema_extra={"example": "true"},
    )
    three_guarantees_reject_flag: bool | None = Field(
        default=None,
        description="Warranty. Warranty",
        json_schema_extra={"example": "false"},
    )
    desc_text: str | None = Field(
        default=None,
        description="Description. Voice-of-customer description",
        json_schema_extra={"example": "riding range well below rated"},
    )
    desc_chars: int | None = Field(
        default=None,
        description="Description. Description",
        json_schema_extra={"example": "86"},
    )
    transcript_text: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "(full call transcript)"},
    )
    agent_id: str | None = Field(
        default=None,
        description="Agent/Outbound call ID. /Outbound call",
        json_schema_extra={"example": "AG-2201"},
    )
    sop_item: str | None = Field(
        default=None,
        description="SOPQuality check. Quality check",
        json_schema_extra={"example": "Confirm VIN and model"},
    )
    sop_pass_fail: SopPassFail | None = Field(
        default=None,
        description="SOPWhether. pass|fail",
        json_schema_extra={"example": "pass"},
    )
    risk_words: Any | None = Field(
        default=None,
        description="Risk. Quality checkRisk",
    )

class VoC(QingshuModel):
    """Service ticket · VoC. Fields from standard field table."""

    feedback_id: str | None = Field(
        default=None,
        description="ID. VoC unique ID",
        json_schema_extra={"example": "FB-99102"},
    )
    nps: float | None = Field(
        default=None,
        description="NPS.",
        json_schema_extra={"example": "32"},
    )
    csat: float | None = Field(
        default=None,
        description="CSAT. 1-5",
        json_schema_extra={"example": "4.1"},
    )
    nps_delta: float | None = Field(
        default=None,
        description="NPS. Week NPS",
        json_schema_extra={"example": "-3"},
    )
    feedback_cnt: int | None = Field(
        default=None,
        description=". Week",
        json_schema_extra={"example": "1280"},
    )
    tag_id: str | None = Field(
        default=None,
        description="TagID. StandardTagID",
        json_schema_extra={"example": "TAG-short-range"},
    )
    tag_name: str | None = Field(
        default=None,
        description="TagName. Tag",
        json_schema_extra={"example": "Short range"},
    )
    tag_domain: TagDomain | None = Field(
        default=None,
        description="Tag domain. product|service|app|channel|risk",
        json_schema_extra={"example": "product"},
    )
    sentiment: Sentiment | None = Field(
        default=None,
        description="Sentiment. pos|neu|neg",
        json_schema_extra={"example": "neg"},
    )
    sentiment_score: float | None = Field(
        default=None,
        description="SentimentScore. Sentiment",
        json_schema_extra={"example": "-0.72"},
    )
    problem_theme: str | None = Field(
        default=None,
        description="Theme. Theme",
        json_schema_extra={"example": "Short range"},
    )
    theme_cnt: int | None = Field(
        default=None,
        description="Theme. Theme",
        json_schema_extra={"example": "246"},
    )
    neg_ratio: float | None = Field(
        default=None,
        description=". Theme",
        json_schema_extra={"example": "68.0"},
    )
    wow_change: float | None = Field(
        default=None,
        description="Week. Week",
        json_schema_extra={"example": "22.0"},
    )
    closed_loop_rate: float | None = Field(
        default=None,
        description="Rate. /",
        json_schema_extra={"example": "54.0"},
    )
    recurrence_rate: float | None = Field(
        default=None,
        description="Rate.",
        json_schema_extra={"example": "12.0"},
    )
    cover_dim: CoverDim | None = Field(
        default=None,
        description=". vehicle|non_vehicle|all",
        json_schema_extra={"example": "vehicle"},
    )
    module_name: ModuleName | None = Field(
        default=None,
        description=". app|miniapp|website|hotline|aftersales",
        json_schema_extra={"example": "app"},
    )
    sample_voice: str | None = Field(
        default=None,
        description="Voice of customer. maskedVoice of customer",
        json_schema_extra={"example": "specification"},
    )
    clue_confidence: ClueConfidence | None = Field(
        default=None,
        description=". weak|medium",
        json_schema_extra={"example": "medium"},
    )
    severity_risk_level: str | None = Field(
        default=None,
        description="Reputation/ RiskLevel. P0|P1|P2",
        json_schema_extra={"example": "P1"},
    )
    consumer_sat_score: float | None = Field(
        default=None,
        description="Consumer. Consumer",
        json_schema_extra={"example": "82.9"},
    )
    channel_sat_score: float | None = Field(
        default=None,
        description="Channel. Channel",
        json_schema_extra={"example": "77.1"},
    )
    survey_recover_rate: float | None = Field(
        default=None,
        description="Rate. /Push",
        json_schema_extra={"example": "6.1"},
    )
    dissatisfaction_reason: str | None = Field(
        default=None,
        description=". /",
        json_schema_extra={"example": "Short range"},
    )
"""JSON strip, Schema validation, post gates."""

from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, Field, ValidationError, field_validator

from shared.tools.guards import BLOCKING_TAGS

_FENCE_RE = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)
_CUS_RE = re.compile(r"CUS-\d+", re.IGNORECASE)
_VIN_RE = re.compile(r"QS0[A-Z0-9]{14}", re.IGNORECASE)
_PHONE_RE = re.compile(r"(?<!\d)(1\d{10})(?!\d)")

BLOCKING_EVIDENCE: list[tuple[str, list[str]]] = [
    ("TAG-open-complaint", ["open complaint", "unresolved", "over 7 days", "multiple complaint", "not resolved", "ticket open"]),
    ("TAG-reputation-risk", ["exposure", "media", "police", "12315", "reputation"]),
    ("TAG-safety-hazard", ["fire", "smoke", "self-ignite", "leak", "safety hazard"]),
]


class TicketDraftV1(BaseModel):
    customer_id: str | None = None
    vin: str | None = None
    ticket_type: str
    fault_category: str | None = None
    consult_category: str | None = None
    ticket_channel: str
    ticket_status: str = "open"
    tag_id: str
    sentiment: str
    desc_text: str = Field(..., min_length=1, max_length=1000)
    is_complaint: bool
    confidence: float | None = None
    needs_human_review: bool | None = None

    @field_validator("ticket_type")
    @classmethod
    def _tt(cls, v: str) -> str:
        allowed = {"fault", "consult", "complaint", "other"}
        if v not in allowed:
            raise ValueError(f"ticket_type : {v}")
        return v

    @field_validator("fault_category")
    @classmethod
    def _fc(cls, v: str | None) -> str | None:
        if v is None:
            return None
        allowed = {
            "battery",
            "motor",
            "brake",
            "controller",
            "charging",
            "dashboard",
            "frame",
            "lighting",
            "tire",
            "other",
        }
        if v not in allowed:
            raise ValueError(f"fault_category : {v}")
        return v

    @field_validator("ticket_channel")
    @classmethod
    def _ch(cls, v: str) -> str:
        allowed = {"400", "App", "E-commerce", "Store", "community"}
        if v not in allowed:
            raise ValueError(f"Invalid ticket_channel: {v}")
        return v

    @field_validator("ticket_status")
    @classmethod
    def _st(cls, v: str) -> str:
        if v not in {"open", "processing", "closed"}:
            raise ValueError(f"ticket_status : {v}")
        return v

    @field_validator("sentiment")
    @classmethod
    def _sent(cls, v: str) -> str:
        if v not in {"pos", "neu", "neg"}:
            raise ValueError(f"sentiment : {v}")
        return v

    @field_validator("customer_id")
    @classmethod
    def _cid(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        if not re.fullmatch(r"CUS-\d+", v):
            raise ValueError("customer_id  CUS-")
        return v

    @field_validator("vin")
    @classmethod
    def _vin(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        vv = v.strip().upper()
        if not re.fullmatch(r"QS0[A-Z0-9]{14}", vv):
            raise ValueError("vin  QS0 + 14 ")
        return vv


class VocEntitiesV1(BaseModel):
    feedback_id: str | None = None
    sample_voice: str = Field(..., min_length=1, max_length=500)
    tag_id: str
    tag_name: str
    tag_domain: str
    sentiment: str
    sentiment_score: float | None = None
    problem_theme: str = Field(..., min_length=1, max_length=64)
    severity_risk_level: str | None = None
    clue_confidence: str
    customer_id: str | None = None
    vin: str | None = None
    secondary_tag_ids: list[str] | None = None
    needs_human_review: bool
    nps: float | None = None
    module_name: str | None = None

    @field_validator("tag_domain")
    @classmethod
    def _dom(cls, v: str) -> str:
        if v not in {"product", "service", "app", "channel", "risk"}:
            raise ValueError(f"tag_domain : {v}")
        return v

    @field_validator("sentiment")
    @classmethod
    def _sent(cls, v: str) -> str:
        if v not in {"pos", "neu", "neg"}:
            raise ValueError(f"sentiment : {v}")
        return v

    @field_validator("clue_confidence")
    @classmethod
    def _cc(cls, v: str) -> str:
        if v not in {"weak", "medium"}:
            raise ValueError(f"clue_confidence : {v}")
        return v

    @field_validator("severity_risk_level")
    @classmethod
    def _sev(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        if v not in {"P0", "P1", "P2"}:
            raise ValueError(f"severity_risk_level : {v}")
        return v

    @field_validator("customer_id")
    @classmethod
    def _cid(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        if not re.fullmatch(r"CUS-\d+", v):
            raise ValueError("customer_id  CUS-")
        return v

    @field_validator("vin")
    @classmethod
    def _vin(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        vv = v.strip().upper()
        if not re.fullmatch(r"QS0[A-Z0-9]{14}", vv):
            raise ValueError("vin  QS0 + 14 ")
        return vv

    @field_validator("secondary_tag_ids")
    @classmethod
    def _sec(cls, v: list[str] | None) -> list[str] | None:
        if not v:
            return []
        if len(v) > 3:
            raise ValueError("secondary_tag_ids  3 ")
        return v

    @field_validator("module_name")
    @classmethod
    def _mod(cls, v: str | None) -> str | None:
        if v is None or v == "":
            return None
        if v not in {"app", "miniapp", "website", "hotline", "aftersales"}:
            raise ValueError(f"module_name : {v}")
        return v


def strip_json_payload(raw: str) -> str:
    text = (raw or "").strip()
    if not text:
        return ""
    m = _FENCE_RE.search(text)
    if m:
        text = m.group(1).strip()
    
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start : end + 1]
    return text


def parse_json_object(raw: str) -> dict[str, Any]:
    body = strip_json_payload(raw)
    if not body:
        raise ValueError(" JSON")
    data = json.loads(body)
    if not isinstance(data, dict):
        raise ValueError(" JSON ")
    return data


def redact_pii(text: str) -> str:
    return _PHONE_RE.sub("***", text or "")


def detect_blocking_tag(text: str) -> str | None:
    for tag_id, kws in BLOCKING_EVIDENCE:
        if any(k in text for k in kws):
            return tag_id
    return None


def apply_known_ids(
    payload: dict[str, Any],
    text: str,
    known: dict[str, Any],
) -> dict[str, Any]:
    out = dict(payload)
    if not out.get("customer_id"):
        if known.get("customer_id"):
            out["customer_id"] = known["customer_id"]
        else:
            m = _CUS_RE.search(text)
            if m:
                digits = re.search(r"\d+", m.group(0))
                if digits:
                    out["customer_id"] = f"CUS-{digits.group(0)}"
    if not out.get("vin"):
        if known.get("vin"):
            out["vin"] = str(known["vin"]).upper()
        else:
            m = _VIN_RE.search(text.upper())
            if m:
                out["vin"] = m.group(0).upper()
    if known.get("channel") and not out.get("ticket_channel"):
        out["ticket_channel"] = known["channel"]
    return out


def validate_payload(
    schema_id: str,
    payload: dict[str, Any],
    *,
    source_text: str,
    allowed_tags: set[str],
    tag_meta: dict[str, dict[str, str]],
) -> tuple[dict[str, Any], list[str]]:
    """( payload, warnings)。 ValueError。"""
    data = dict(payload)
    warnings: list[str] = []

    
    if "desc_text" in data and isinstance(data["desc_text"], str):
        data["desc_text"] = redact_pii(data["desc_text"])[:1000]
    if "sample_voice" in data and isinstance(data["sample_voice"], str):
        data["sample_voice"] = redact_pii(data["sample_voice"])[:500]

    # tag ：
    hit = detect_blocking_tag(source_text)
    if hit:
        primary = str(data.get("tag_id") or "")
        secondary = list(data.get("secondary_tag_ids") or [])
        if primary not in BLOCKING_TAGS and hit not in secondary:
            if schema_id == "voc_entities_v1" and primary and primary not in BLOCKING_TAGS:
                secondary = ([hit] + [x for x in secondary if x != hit])[:3]
                data["secondary_tag_ids"] = secondary
                data["needs_human_review"] = True
                warnings.append(f"injected_blocking_secondary:{hit}")
            else:
                data["tag_id"] = hit
                if schema_id == "ticket_draft_v1":
                    data["is_complaint"] = True
                    data["sentiment"] = "neg"
                    data["ticket_type"] = data.get("ticket_type") or "complaint"
                    if data["ticket_type"] == "fault":
                        data["ticket_type"] = "complaint"
                warnings.append(f"forced_blocking_tag:{hit}")

    if schema_id == "ticket_draft_v1":
        model = TicketDraftV1.model_validate(data)
        out = model.model_dump()
    elif schema_id == "voc_entities_v1":
        model = VocEntitiesV1.model_validate(data)
        out = model.model_dump()
    else:
        raise ValueError(f"schema_id: {schema_id}")

    tag_id = out.get("tag_id")
    if not tag_id or tag_id not in allowed_tags:
        raise ValueError(f"tag_id tagdictionary: {tag_id}")

    if schema_id == "voc_entities_v1":
        meta = tag_meta.get(str(tag_id), {})
        if meta.get("tag_name") and out.get("tag_name") != meta["tag_name"]:
            out["tag_name"] = meta["tag_name"]
            warnings.append("normalized_tag_name")
        if meta.get("tag_domain") and out.get("tag_domain") != meta["tag_domain"]:
            out["tag_domain"] = meta["tag_domain"]
            warnings.append("normalized_tag_domain")
        for sid in list(out.get("secondary_tag_ids") or []):
            if sid not in allowed_tags:
                raise ValueError(f"secondary tag dictionary: {sid}")

    # ID →
    if out.get("customer_id") is None and out.get("vin") is None:
        out["needs_human_review"] = True

    return out, warnings


def format_validation_error(exc: Exception) -> str:
    if isinstance(exc, ValidationError):
        parts = []
        for err in exc.errors():
            loc = ".".join(str(x) for x in err.get("loc", ()))
            parts.append(f"{loc}: {err.get('msg')}")
        return "; ".join(parts) or str(exc)
    return str(exc)
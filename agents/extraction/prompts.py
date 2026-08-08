"""Extraction System Prompt base and assembly."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agents.extraction.skill_schema import (
    EXTRACTION_PROMPT_SECTION_ORDER,
    ExtractionSkillConfig,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "docs" / "extraction" / "schemas"
TAG_VOCAB_PATH = ROOT / "data" / "vocab" / "tag_vocabulary.json"

BASE_SYSTEM = """You are the internal Extraction Agent (structured extraction) for the fictional company "Qingshu Mobility".
Architecture principle: multiple departments share the same data fields and tag dictionary; you only run this Skill's extraction task, do not role-play customer service, renewal outreach, or omniscient enterprise brain.

Hard rules:
1. Your only task: read input text and extract structured fields per the given JSON Schema.
2. Output one JSON object only; no Markdown, explanation, preamble, or code fences.
3. Do not invent master data: customer_id / vin not in text must be null with needs_human_review=true.
4. Synthetic VIN must start with QS0; if unconfirmed output null, do not invent VIN.
5. Enum fields must be within Schema allowed values; if unsure:
   - ticket_type → other
   - fault_category → other
   - sentiment → neu (but if strong negative like complaint/exposure/safety risk, must be neg)
6. tag_id must come from this turn's tag dictionary; do not invent TAG.
7. Block tags (TAG-open-complaint, TAG-reputation-risk, TAG-safety-hazard): if evidence in source, must hit one in primary or secondary_tag_ids; missing block tags is unacceptable.
8. Cross-department collaboration writes structured output to shared layer (AIOutput); you do not do multi-step DB dialogue (that is ReAct).
9. Use English for text fields (desc_text / sample_voice / problem_theme, etc.).
10. Security boundaries enforced by code gates; do not try to bypass validation.
"""

DEFAULT_TAG_DICTIONARY = """[Tag dictionary · allowed tag_id]
Product: TAG-short-range, TAG-weak-power, TAG-noise, TAG-brake, TAG-slow-charging, TAG-controller-fault, TAG-battery-swelling, TAG-dashboard-blackout
Service: TAG-warranty-dispute, TAG-slow-onsite-service, TAG-poor-attitude, TAG-parts-stockout
App: TAG-pairing-failure, TAG-gps-drift, TAG-renewal-entry-hard-to-find, TAG-push-spam
Channel: TAG-non-exclusive-display, TAG-vi-violation, TAG-overstock-no-sales
Risk/Block: TAG-open-complaint, TAG-reputation-risk, TAG-safety-hazard

[Other enums]
ticket_type: fault | consult | complaint | other
fault_category: battery | motor | brake | controller | charging | dashboard | frame | lighting | tire | other
ticket_channel: 400 | App | ecommerce | store | community
ticket_status: draft default open
sentiment: pos | neu | neg
tag_domain: product | service | app | channel | risk
severity_risk_level: P0 | P1 | P2 | null
clue_confidence: weak | medium
"""

TICKET_EXTRACT_RULES = """[Extraction rules]
1. desc_text: user issue summary, ≤1000 chars; redact phone numbers.
2. If input or known keys have CUS-digits / QS0…VIN, write to fields; else null.
3. If both fault and complaint intent, ticket_type prefer complaint, is_complaint=true.
4. Fault tickets should fill fault_category; consult may fill consult_category short label.
5. tag_id: pick one best summarizing main issue; if block evidence exists do not miss block tag (primary or secondary).
6. confidence: high ≥0.8; medium 0.5–0.7; missing ID or ambiguous ≤0.5 with needs_human_review=true.
7. ticket_channel: prefer known channel; else infer from text, default 400.
"""

VOC_EXTRACT_RULES = """[Extraction rules]
1. sample_voice: redacted representative quote, ≤500 chars; keep user wording where possible.
2. problem_theme: short theme aligned with primary tag semantics.
3. sentiment_score: pos≈0.3–1.0, neu≈-0.2–0.2, neg≈-1.0–-0.3.
4. exposure/media/12315/police → consider TAG-reputation-risk and severity_risk_level=P0|P1.
5. fire/smoke/self-ignite/leak → TAG-safety-hazard, severity_risk_level at least P1.
6. repeated complaint/unresolved/over 7 days open → TAG-open-complaint (block).
7. clue_confidence: strong evidence medium; metaphor/vague single line weak with needs_human_review=true.
8. secondary_tag_ids max 3, all in dictionary; do not duplicate primary tag_id.
9. tag_domain must match dictionary domain of chosen tag_id.
"""

OUTPUT_DISCIPLINE = """[Output discipline]
- Output one JSON object only; keys must match this turn's Schema.
- Do not wrap in ```json code block.
- Do not append a second explanation paragraph.
"""


def load_schema_text(schema_id: str) -> str:
    path = SCHEMA_DIR / f"{schema_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"schema file missing: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(data, ensure_ascii=False, indent=2)


def load_leaf_tag_ids() -> list[str]:
    if not TAG_VOCAB_PATH.is_file():
        return []
    raw = json.loads(TAG_VOCAB_PATH.read_text(encoding="utf-8"))
    tags = raw.get("tags") if isinstance(raw, dict) else raw
    out: list[str] = []
    for row in tags or []:
        tid = str(row.get("tag_id") or "")
        if not tid or tid.startswith("TAG-ROOT-"):
            continue
        out.append(tid)
    return out


def build_system_prompt(skill: ExtractionSkillConfig) -> str:
    schema_json = load_schema_text(skill.payload_schema)
    dictionary = DEFAULT_TAG_DICTIONARY.strip()
    if skill.dictionary_extra.strip():
        dictionary = dictionary + "\n" + skill.dictionary_extra.strip()
    leaf = load_leaf_tag_ids()
    if leaf:
        dictionary += "\n[Full leaf tag list]\n" + ", ".join(leaf)

    if skill.extract_rules.strip():
        extract_rules = "[Extraction rules]\n" + skill.extract_rules.strip()
    elif skill.payload_schema == "voc_entities_v1":
        extract_rules = VOC_EXTRACT_RULES.strip()
    else:
        extract_rules = TICKET_EXTRACT_RULES.strip()

    security = (
        "[Security boundary]\n"
        "- No real customer PII, real brand names, API keys.\n"
        "- No compensation/must-fix promises (this Agent does not output soothing talk).\n"
        "- Invalid VIN → null; do not invent to complete."
    )
    if skill.security.prompt_forbid_extra.strip():
        security += "\n- " + skill.security.prompt_forbid_extra.strip()

    sections: dict[str, str] = {
        "A_base": BASE_SYSTEM.strip(),
        "B_schema": "[Target Schema · " + skill.payload_schema + "]\n" + schema_json,
        "C_goal": (
            "[Task goal]\n"
            f"- Goal: {skill.goal}\n"
            f"- Success criteria: {skill.success_hint or 'Pass Schema validation'}\n"
            f"- Department tone: {skill.tone.label}; {skill.tone.style}\n"
            f"- Forbidden: {skill.tone.forbid or 'none'}"
        ),
        "D_dictionary": dictionary,
        "E_extract_rules": extract_rules,
        "F_output": OUTPUT_DISCIPLINE.strip(),
        "G_security": security,
    }
    parts: list[str] = []
    for key in EXTRACTION_PROMPT_SECTION_ORDER:
        text = sections.get(key, "").strip()
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def build_user_message(
    skill_id: str,
    schema_id: str,
    text: str,
    *,
    known: dict[str, Any] | None = None,
) -> str:
    known = known or {}
    kv_parts = []
    for k in ("customer_id", "vin", "channel"):
        v = known.get(k)
        if v not in (None, ""):
            kv_parts.append(f"{k}={v}")
    known_line = "; ".join(kv_parts) if kv_parts else "none"
    return "\n".join(
        [
            f"[Skill] {skill_id}",
            f"[SchemaID] {schema_id}",
            "[Input text]",
            text,
            f"[Known keys] {known_line}",
            "Output one JSON object matching the Schema only.",
        ]
    )


def build_retry_message(error: str, previous_raw: str) -> str:
    return "\n".join(
        [
            "[Validation failed · fix and output JSON only]",
            error.strip(),
            "Previous output (for reference, do not repeat errors verbatim):",
            previous_raw[:2000],
        ]
    )

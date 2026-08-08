"""（V2）· ID 。 （ / AGENT_TYPES / OpenAPI meta）： retrieve | act | extract | plan （Skill YAML、 API 、CLI、 FEATURES ）： rag | react | extraction | planning （ ， AGENT_TYPES）： rule_llm → Plan vision → Extract"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------

PLATFORM_LOOPS: tuple[str, ...] = ("retrieve", "act", "extract", "plan")

LOOP_META: dict[str, dict[str, Any]] = {
    "retrieve": {
        "name": "Retrieve（search）",
        "legacy": "rag",
        "status": "ready",
        "blurb": " Retrieve：retrieve → stuff → generate → cite。Skill：repair_kb / policy_kb / hr_rules。",
        "dir": "agents/rag/",
        "api_path": "/v1/rag/runs",
    },
    "act": {
        "name": "Act（）",
        "legacy": "react",
        "status": "ready",
        "blurb": " Act：think → act → observe。Skill：fill_ticket / crm_lookup / channel_ops 。",
        "dir": "agents/react/",
        "api_path": "/v1/react/runs",
    },
    "extract": {
        "name": "Extract（）",
        "legacy": "extraction",
        "status": "ready",
        "blurb": " Extract：schema → extract → validate。Skill：ticket_fields / voc_entities。",
        "dir": "agents/extraction/",
        "api_path": "/v1/extraction/runs",
    },
    "plan": {
        "name": "Plan（）",
        "legacy": "planning",
        "status": "ready",
        "blurb": " Plan：shared → /。Skill：renewal_plan（Story2）。API：POST /v1/planning/runs  POST /v1/runs + control_loop=plan。",
        "dir": "agents/planning/",
        "api_path": "/v1/planning/runs",
    },
}

# → （ ）
AGENT_TYPE_ALIASES: dict[str, str] = {
    "rag": "retrieve",
    "react": "act",
    "extraction": "extract",
    "planning": "plan",
    # ， resolve
    "retrieve": "retrieve",
    "act": "act",
    "extract": "extract",
    "plan": "plan",
}

# → （API / Skill YAML ）
LOOP_TO_LEGACY: dict[str, str] = {
    "retrieve": "rag",
    "act": "react",
    "extract": "extraction",
    "plan": "planning",
}

# ： ，
EXTENSION_TYPES: dict[str, dict[str, Any]] = {
    "rule_llm": {
        "name": " · ",
        "parent_loop": "plan",
        "status": "planned",
        "blurb": " Plan ；。",
    },
    "vision": {
        "name": " · ",
        "parent_loop": "extract",
        "status": "planned",
        "blurb": " Extract ；Phase 3，。",
    },
}

DISPLAY_NAMES: dict[str, str] = {
    "retrieve": "Retrieve",
    "act": "Act",
    "extract": "Extract",
    "plan": "Plan",
    "rag": "Retrieve",
    "react": "Act",
    "extraction": "Extract",
    "planning": "Plan",
    "rule_llm": "",
    "vision": "",
}


def canonicalize(agent_type: str | None) -> str | None:
    """/ → loop id； type ； 。"""
    if agent_type is None:
        return None
    key = str(agent_type).strip()
    if not key:
        return None
    if key in AGENT_TYPE_ALIASES:
        return AGENT_TYPE_ALIASES[key]
    if key in EXTENSION_TYPES:
        return key
    return key


def to_legacy(agent_type: str | None) -> str | None:
    """→ ； ； type 。"""
    if agent_type is None:
        return None
    key = str(agent_type).strip()
    canon = canonicalize(key)
    if canon in LOOP_TO_LEGACY:
        return LOOP_TO_LEGACY[canon]
    return key


def is_platform_loop(agent_type: str | None) -> bool:
    return canonicalize(agent_type) in PLATFORM_LOOPS


def same_loop(a: str | None, b: str | None) -> bool:
    """Either side legacy or canonical name; compare loops as equivalent."""
    ca, cb = canonicalize(a), canonicalize(b)
    if ca is None or cb is None:
        return False
    return ca == cb


def display_name(agent_type: str | None) -> str:
    if not agent_type:
        return ""
    return DISPLAY_NAMES.get(agent_type, DISPLAY_NAMES.get(canonicalize(agent_type) or "", agent_type))


def aliases_for(loop_id: str) -> list[str]:
    """（ ）。"""
    legacy = LOOP_TO_LEGACY.get(loop_id)
    return [legacy] if legacy else []


def build_agent_types() -> list[dict[str, Any]]:
    """catalog.AGENT_TYPES （ ）。"""
    out: list[dict[str, Any]] = []
    for loop_id in PLATFORM_LOOPS:
        meta = LOOP_META[loop_id]
        out.append(
            {
                "agent_type": loop_id,
                "loop_id": loop_id,
                "name": meta["name"],
                "status": meta["status"],
                "blurb": meta["blurb"],
                "legacy_alias": meta["legacy"],
                "aliases": aliases_for(loop_id),
                "manage_separately": True,
            }
        )
    return out


def meta_payload() -> dict[str, Any]:
    """OpenAPI /v1/meta 。"""
    ready = [lid for lid in PLATFORM_LOOPS if LOOP_META[lid]["status"] == "ready"]
    return {
        "control_loops": list(PLATFORM_LOOPS),
        "agent_types_ready": ready,
        "agent_type_aliases": {
            k: v for k, v in AGENT_TYPE_ALIASES.items() if k != v
        },
        "loop_to_legacy": dict(LOOP_TO_LEGACY),
        "legacy_api_paths": {lid: LOOP_META[lid]["api_path"] for lid in PLATFORM_LOOPS},
        "unified_runs_api": "/v1/runs",
        "extension_types": {
            k: {"parent_loop": v["parent_loop"], "status": v["status"]}
            for k, v in EXTENSION_TYPES.items()
        },
    }
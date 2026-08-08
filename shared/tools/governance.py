"""（V2）· 。 （ / OpenAPI / ）： read | knowledge | write_govern ToolSpec.category（ domain）： master | commerce | service | renewal | knowledge | shared | channel | iot … handler ； 。"""

from __future__ import annotations

from typing import Any

TOOL_CLASSES: tuple[str, ...] = ("read", "knowledge", "write_govern")

TOOL_CLASS_META: dict[str, dict[str, Any]] = {
    "read": {
        "name": "Read（）",
        "blurb": " /  /  / renewal / channel / IoT lookup。",
    },
    "knowledge": {
        "name": "Knowledge（search）",
        "blurb": "searchdocumentread；Retrieve 。",
    },
    "write_govern": {
        "name": "Write/Govern（shared）",
        "blurb": "Shared output、sharedtag、、、run。",
    },
}

# （ domain ）
KNOWLEDGE_TOOLS: frozenset[str] = frozenset(
    {
        "search_kb",
        "get_kb_document",
        "list_kb_domains",
    }
)

WRITE_GOVERN_TOOLS: frozenset[str] = frozenset(
    {
        "write_ai_output",
        "read_ai_outputs",
        "read_shared_tags",
        "get_ai_output",
        "check_outreach_block",
        "list_capabilities",
        "get_capability",
        "log_step",
        "list_run_logs",
    }
)

# domain category → tool_class（ ）
_DOMAIN_DEFAULT_CLASS: dict[str, str] = {
    "knowledge": "knowledge",
    "shared": "write_govern",
    "master": "read",
    "commerce": "read",
    "service": "read",
    "renewal": "read",
    "channel": "read",
    "iot": "read",
    "general": "read",
}


def resolve_tool_class(name: str, domain_category: str | None = None) -> str:
    """+ optional domain → 。"""
    if name in KNOWLEDGE_TOOLS:
        return "knowledge"
    if name in WRITE_GOVERN_TOOLS:
        return "write_govern"
    if domain_category:
        mapped = _DOMAIN_DEFAULT_CLASS.get(domain_category)
        if mapped:
            # shared domain write_govern （ get_tag） read
            if domain_category == "shared" and name not in WRITE_GOVERN_TOOLS:
                return "read"
            return mapped
    return "read"


def classify_all(tool_rows: list[dict[str, Any]]) -> dict[str, list[str]]:
    """tool_class （ summary）。"""
    out: dict[str, list[str]] = {c: [] for c in TOOL_CLASSES}
    for row in tool_rows:
        name = row.get("name") or ""
        tc = row.get("tool_class") or resolve_tool_class(name, row.get("category"))
        if tc not in out:
            out[tc] = []
        out[tc].append(name)
    for c in out:
        out[c].sort()
    return out


def meta_payload() -> dict[str, Any]:
    """/v1/meta 。"""
    return {
        "tool_classes": list(TOOL_CLASSES),
        "tool_class_meta": {
            k: {"name": v["name"], "blurb": v["blurb"]} for k, v in TOOL_CLASS_META.items()
        },
    }


def ledger_snapshot() -> dict[str, Any]:
    """（write JSON API）。"""
    return {
        "version": "v2",
        "tool_classes": list(TOOL_CLASSES),
        "knowledge_tools": sorted(KNOWLEDGE_TOOLS),
        "write_govern_tools": sorted(WRITE_GOVERN_TOOLS),
        "note": " tool_class=read；domain ToolSpec.category。",
    }
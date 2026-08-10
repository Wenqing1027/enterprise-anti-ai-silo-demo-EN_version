"""DeepSeek / OpenAI compatible tool_calls parse contract.

Supports:
1) OpenAI-style message.tool_calls (preferred)
2) DeepSeek DSML text in message.content (fallback), e.g.
   <｜DSML｜tool_calls>
   <｜DSML｜invoke name="get_dealer_health">
   <｜DSML｜parameter name="dealer_id" string="true">DLR-3017</｜DSML｜parameter>
   </｜DSML｜invoke>
   </｜DSML｜tool_calls>
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ParsedToolCall:
    id: str
    name: str
    arguments: dict[str, Any]
    arguments_raw: str


_INVOKE_RE = re.compile(
    r'invoke\s+name\s*=\s*"([^"]+)"\s*>(.*?)(?:</[^<>]*invoke>|$)',
    re.IGNORECASE | re.DOTALL,
)
_PARAM_RE = re.compile(
    r'parameter\s+name\s*=\s*"([^"]+)"(?:\s+string\s*=\s*"(true|false)")?\s*>'
    r'(.*?)</[^<>]*parameter>',
    re.IGNORECASE | re.DOTALL,
)
_DSML_BLOCK_RE = re.compile(
    r"(?:tool_calls|function_calls)\s*>(.*?)(?:</[^<>]*(?:tool_calls|function_calls)>|$)",
    re.IGNORECASE | re.DOTALL,
)


def looks_like_dsml(text: str | None) -> bool:
    if not text:
        return False
    s = str(text)
    return ("DSML" in s and "invoke" in s.lower()) or (
        "invoke name=" in s.lower() and "parameter name=" in s.lower()
    )


def _normalize_param_key(key: str) -> str:
    """Map DSML display names like 'Customer ID' → customer_id."""
    k = (key or "").strip()
    k = re.sub(r"[\s\-]+", "_", k)
    return k.lower()


def strip_dsml(text: str | None) -> str:
    """Remove DSML tool markup; keep any plain prose before/after."""
    if not text:
        return ""
    s = str(text).replace("｜", "|")
    # Drop whole tool_calls / function_calls blocks first
    s = re.sub(
        r"<?\s*\|\s*\|\s*DSML\s*\|\s*\|\s*(?:tool_calls|function_calls)\s*>.*?"
        r"(?:</\s*\|\s*\|\s*DSML\s*\|\s*\|\s*(?:tool_calls|function_calls)\s*>|$)",
        "",
        s,
        flags=re.IGNORECASE | re.DOTALL,
    )
    s = re.sub(
        r"<\|DSML\|(?:tool_calls|function_calls)>.*?(?:</\|DSML\|(?:tool_calls|function_calls)>|$)",
        "",
        s,
        flags=re.IGNORECASE | re.DOTALL,
    )
    # Drop any remaining DSML tags
    s = re.sub(r"</?\s*\|\s*\|\s*DSML\s*\|\s*\|\s*[^>]*>", "", s, flags=re.IGNORECASE)
    s = re.sub(r"</?\|DSML\|[^>]*>", "", s, flags=re.IGNORECASE)
    return s.strip()


def parse_arguments(raw: Any) -> tuple[dict[str, Any], str, bool]:
    """Return (args_dict, raw_str, ok). ok=False when JSON object parse failed."""
    if raw is None:
        return {}, "{}", True
    if isinstance(raw, dict):
        return dict(raw), json.dumps(raw, ensure_ascii=False), True
    if not isinstance(raw, str):
        raw = str(raw)
    text = raw.strip() or "{}"
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return {"_raw": text}, text, False
    if isinstance(data, dict):
        return data, text, True
    return {"_raw": text}, text, False


def extract_dsml_tool_calls(content: str | None) -> list[ParsedToolCall]:
    """Parse DeepSeek DSML tool markup from assistant content text."""
    if not content or not looks_like_dsml(content):
        return []

    # Normalize fullwidth / spaced DSML markers to a simple form for regex
    text = str(content)
    text = text.replace("｜", "|")
    text = re.sub(r"<\s*\|\s*\|\s*DSML\s*\|\s*\|\s*", "<|DSML|", text)
    text = re.sub(r"</\s*\|\s*\|\s*DSML\s*\|\s*\|\s*", "</|DSML|", text)
    text = re.sub(r"\|\s*\|\s*DSML\s*\|\s*\|", "|DSML|", text)

    blocks = _DSML_BLOCK_RE.findall(text)
    body = "\n".join(blocks) if blocks else text

    out: list[ParsedToolCall] = []
    for i, m in enumerate(_INVOKE_RE.finditer(body)):
        name = (m.group(1) or "").strip()
        inner = m.group(2) or ""
        if not name:
            continue
        args: dict[str, Any] = {}
        for pm in _PARAM_RE.finditer(inner):
            key = _normalize_param_key(pm.group(1) or "")
            is_string = (pm.group(2) or "true").lower() == "true"
            val_raw = (pm.group(3) or "").strip()
            if not key:
                continue
            if is_string:
                args[key] = val_raw
            else:
                try:
                    args[key] = json.loads(val_raw)
                except json.JSONDecodeError:
                    args[key] = val_raw
        raw_str = json.dumps(args, ensure_ascii=False)
        out.append(
            ParsedToolCall(
                id=f"call_dsml_{i}",
                name=name,
                arguments=args,
                arguments_raw=raw_str,
            )
        )
    return out


def extract_tool_calls(message: Any) -> list[ParsedToolCall]:
    """Extract tool_calls from OpenAI SDK message/dict, with DSML content fallback."""
    raw_calls = getattr(message, "tool_calls", None)
    if raw_calls is None and isinstance(message, dict):
        raw_calls = message.get("tool_calls")

    out: list[ParsedToolCall] = []
    if raw_calls:
        for i, tc in enumerate(raw_calls):
            if isinstance(tc, dict):
                tc_id = str(tc.get("id") or f"call_auto_{i}")
                fn = tc.get("function") or {}
                name = str(fn.get("name") or "")
                args_raw = fn.get("arguments")
            else:
                tc_id = str(getattr(tc, "id", None) or f"call_auto_{i}")
                fn = getattr(tc, "function", None)
                name = str(getattr(fn, "name", None) or "")
                args_raw = getattr(fn, "arguments", None) if fn is not None else None
            args, raw_str, _ok = parse_arguments(args_raw)
            if not name:
                continue
            out.append(
                ParsedToolCall(
                    id=tc_id,
                    name=name,
                    arguments=args,
                    arguments_raw=raw_str,
                )
            )
        if out:
            return out

    content = getattr(message, "content", None)
    if content is None and isinstance(message, dict):
        content = message.get("content")
    return extract_dsml_tool_calls(content)


def assistant_tool_call_message(
    content: str | None, calls: list[ParsedToolCall]
) -> dict[str, Any]:
    """Build assistant message with tool_calls for the next LLM turn."""
    # Do not echo raw DSML markup back into the conversation.
    clean = strip_dsml(content) if looks_like_dsml(content) else (content or "")
    return {
        "role": "assistant",
        "content": clean or "",
        "tool_calls": [
            {
                "id": c.id,
                "type": "function",
                "function": {
                    "name": c.name,
                    "arguments": c.arguments_raw,
                },
            }
            for c in calls
        ],
    }


def tool_result_message(call_id: str, observation: dict[str, Any], *, limit: int = 8000) -> dict[str, Any]:
    body = json.dumps(observation, ensure_ascii=False, default=str)
    if len(body) > limit:
        body = body[:limit] + "…"
    return {
        "role": "tool",
        "tool_call_id": call_id,
        "content": body,
    }


def allows_empty_args(tool_name: str) -> bool:
    """Whether list_* tools may be called with empty args."""
    if tool_name.startswith("list_"):
        return True
    return tool_name in {"list_capabilities"}

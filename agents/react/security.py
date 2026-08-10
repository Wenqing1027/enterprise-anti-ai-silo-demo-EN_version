"""ReAct module 4: Skill security precheck and observation redaction."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from agents.react.skill_schema import SkillConfig, SkillSecurity

_PHONE_RE = re.compile(r"(?<!\*)(1[3-9]\d{9})(?!\*)")
_SECRET_RE = re.compile(
    r"(?i)(sk-[a-z0-9]{10,}|api[_-]?key\s*[:=]\s*\S+|deepseek_api_key\s*[:=]\s*\S+|bearer\s+[a-z0-9\-._]+)"
)


@dataclass
class SecurityVerdict:
    allow: bool
    code: str | None = None
    message: str | None = None
    args: dict[str, Any] | None = None


def precheck_tool_calls_count(skill: SkillConfig, n_calls: int) -> SecurityVerdict:
    sec = skill.security
    cap = sec.max_tool_calls_per_step
    if n_calls > cap:
        return SecurityVerdict(
            allow=False,
            code="TOO_MANY_TOOL_CALLS",
            message=f"tool_calls={n_calls} {cap}",
        )
    return SecurityVerdict(allow=True)


def precheck_tool_args(
    skill: SkillConfig,
    tool_name: str,
    args: dict[str, Any],
    *,
    fetcher: Any | None = None,
) -> SecurityVerdict:
    """Registry Skill （ Registry ）。 ：search_kb / domain；get_kb_document domain doc_id 。"""
    sec = skill.security
    cleaned = dict(args)
    allow = list(sec.kb_domains_allow)

    if not allow:
        return SecurityVerdict(allow=True, args=cleaned)

    if tool_name == "search_kb":
        domain = cleaned.get("domain")
        if domain is None or str(domain).strip() == "":
            if len(allow) == 1:
                cleaned["domain"] = allow[0]
            else:
                return SecurityVerdict(
                    allow=False,
                    code="KB_DOMAIN_REQUIRED",
                    message=f"domain，allowed：{allow}",
                )
        else:
            d = str(domain).strip().lower()
            if d not in allow:
                return SecurityVerdict(
                    allow=False,
                    code="KB_DOMAIN_DENIED",
                    message=f"domain={d} Skill alloweddomain {allow}",
                )
            cleaned["domain"] = d
        return SecurityVerdict(allow=True, args=cleaned)

    if tool_name == "get_kb_document":
        doc_id = cleaned.get("kb_doc_id")
        if not doc_id:
            return SecurityVerdict(allow=True, args=cleaned)
        if fetcher is None:
            return SecurityVerdict(
                allow=False,
                code="KB_DOMAIN_CHECK_UNAVAILABLE",
                message="validation kb domain： fetcher",
            )
        row = fetcher.get_kb_document(str(doc_id))
        if row is None:
            return SecurityVerdict(allow=True, args=cleaned)
        domain = getattr(row, "kb_domain", None)
        if domain is None and isinstance(row, dict):
            domain = row.get("kb_domain")
        d = str(domain or "").strip().lower()
        if d not in allow:
            return SecurityVerdict(
                allow=False,
                code="KB_DOMAIN_DENIED",
                message=f"documentdomain={d or '?'} Skill alloweddomain {allow}",
            )
        return SecurityVerdict(allow=True, args=cleaned)

    if tool_name == "list_kb_domains":
        # ； tool handler + context.kb_domains_allow
        return SecurityVerdict(allow=True, args=cleaned)

    return SecurityVerdict(allow=True, args=cleaned)


def should_stop_for_outreach(skill: SkillConfig, tool_name: str, result_data: Any) -> SecurityVerdict:
    if not skill.security.block_on_outreach:
        return SecurityVerdict(allow=True)
    if tool_name != "check_outreach_block":
        return SecurityVerdict(allow=True)
    if not isinstance(result_data, dict):
        return SecurityVerdict(allow=True)
    if result_data.get("blocked") or result_data.get("allow_outreach") is False:
        reason = result_data.get("block_reason") or "tag"
        return SecurityVerdict(
            allow=False,
            code="OUTREACH_BLOCKED",
            message=f"：{reason}",
        )
    return SecurityVerdict(allow=True)


def redact_pii_text(text: str) -> str:
    text = _PHONE_RE.sub("1**********", text)
    text = _SECRET_RE.sub("[REDACTED_SECRET]", text)
    return text


def sanitize_observation(
    observation: dict[str, Any],
    skill: SkillConfig,
) -> dict[str, Any]:
    if not skill.security.redact_pii_in_observation:
        return observation
    import json

    raw = json.dumps(observation, ensure_ascii=False, default=str)
    redacted = redact_pii_text(raw)
    if redacted == raw:
        return observation
    try:
        return json.loads(redacted)
    except json.JSONDecodeError:
        return {"ok": observation.get("ok"), "redacted": True, "content": redacted}


def build_security_prompt_section(skill: SkillConfig) -> str:
    sec: SkillSecurity = skill.security
    lines = [
        "[Security boundaries]",
        "- Do not output or echo API keys / passwords / plaintext phone numbers.",
        "- Do not invent facts not returned by tools; synthetic VIN must use QS0 prefix.",
        f"- At most {sec.max_tool_calls_per_step} tool_calls per step.",
    ]
    if sec.kb_domains_allow:
        lines.append(f"- Knowledge domains allowed: {', '.join(sec.kb_domains_allow)}.")
    if sec.block_on_outreach:
        lines.append(
            "- If check_outreach_block reports blocked, stop outreach wording immediately."
        )
    if sec.prompt_forbid_extra.strip():
        lines.append(f"- Extra forbid: {sec.prompt_forbid_extra.strip()}")
    if skill.tone.forbid.strip():
        lines.append(f"- Tone forbid (restate): {skill.tone.forbid.strip()}")
    return "\n".join(lines)

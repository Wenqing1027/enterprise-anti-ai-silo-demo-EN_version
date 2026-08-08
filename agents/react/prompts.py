"""ReAct System Prompt base and assembly (section order fixed by PROMPT_SECTION_ORDER)."""

from __future__ import annotations

from typing import Any

from agents.react.security import build_security_prompt_section
from agents.react.skill_schema import PROMPT_SECTION_ORDER, SkillConfig

BASE_SYSTEM = """You are the internal ReAct Agent (Tool-Calling) for the fictional company "Qingshu Mobility".
Architecture principle: multiple departments share the same tools and data access; you only play this Skill's department role, do not impersonate an omniscient enterprise brain.

Hard rules:
1. Facts must come from tool returns; do not invent customers, vehicles, inventory, policy, rebate numbers.
2. Only call tools on this turn's allowlist; do not request tools not provided.
3. Cross-department collaboration uses write_ai_output / read_ai_outputs / read_shared_tags; do not pretend private DBs exist.
4. Synthetic VIN must start with QS0; on invalid VIN explain and stop inventing.
5. Think before each tool call; when information is enough give final answer (no more tools).
6. Final answer in English, matching this Skill tone, concise and actionable.
7. Security boundaries enforced by code gates; do not bypass tool error codes and keep inventing results.
"""


def build_system_prompt(skill: SkillConfig | dict[str, Any], tool_names: list[str]) -> str:
    """Assemble in PROMPT_SECTION_ORDER; do not reorder at call sites."""
    if isinstance(skill, SkillConfig):
        cfg = skill
    else:
        cfg = SkillConfig.model_validate(skill)

    sections: dict[str, str] = {
        "A_base": BASE_SYSTEM.strip(),
        "B_tone": (
            "[Department tone]\n"
            f"- Style label: {cfg.tone.label}\n"
            f"- Points: {cfg.tone.style}\n"
            f"- Forbidden: {cfg.tone.forbid}"
        ),
        "C_goal": (
            "[Task goal]\n"
            f"- Goal: {cfg.goal}\n"
            f"- Success criteria: {cfg.success_hint or cfg.success_when}"
        ),
        "C2_system_extra": (
            ("[Skill supplement]\n" + cfg.system_extra.strip()) if cfg.system_extra.strip() else ""
        ),
        "D_tools": (
            "[Tool constraints]\n"
            f"- Available tools: {', '.join(tool_names)}\n"
            "- Tool results are observations; on failure adjust per error, do not repeat invalid calls more than 2 times."
        ),
        "E_output": (
            ("[Final answer format]\n" + cfg.output_format.strip()) if cfg.output_format.strip() else ""
        ),
        "F_security": build_security_prompt_section(cfg),
    }

    parts: list[str] = []
    for key in PROMPT_SECTION_ORDER:
        text = sections.get(key, "").strip()
        if text:
            parts.append(text)
    return "\n\n".join(parts)


def build_user_message(
    skill_id: str,
    text: str,
    *,
    known: dict[str, Any] | None = None,
) -> str:
    lines = [
        f"[Skill] {skill_id}",
        f"[Input] {text}",
    ]
    if known:
        kv = ", ".join(f"{k}={v}" for k, v in known.items() if v not in (None, ""))
        if kv:
            lines.append(f"[Known keys] {kv}")
    lines.append("Complete task within tool allowlist; give final answer when success criteria met.")
    return "\n".join(lines)

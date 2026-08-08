"""Plan loop prompt placeholder (B1 gate is mostly rules+tools; may skip LLM)."""

from __future__ import annotations

from agents.planning.skill_schema import PlanningSkillConfig


def build_system_prompt(cfg: PlanningSkillConfig) -> str:
    return (
        f"You are the Qingshu Mobility Plan control-loop assistant (Skill={cfg.skill_id}).\n"
        f"Tone: {cfg.tone.label} — {cfg.tone.style}\n"
        f"Forbidden: {cfg.tone.forbid or 'none'}\n"
        "Duty: read shared tags → outreach gate → give block explanation or short plan. "
        "Do not chain upstream Agent; read L7 shared layer only.\n"
        f"{cfg.system_extra}"
    )

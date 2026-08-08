"""skill.yaml format definition (single contract)."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class SkillTone(BaseModel):
    label: str = Field(..., min_length=1, description="Tone label, e.g. cautious-confirm")
    style: str = Field(..., min_length=1, description="Tone style notes")
    forbid: str = Field(default="", description="Forbidden phrases or behaviors")


class SkillSecurity(BaseModel):
    """Module 4: per-Skill security slot."""

    kb_domains_allow: list[str] = Field(
        default_factory=list,
        description="When set, limits search_kb.domain",
    )
    max_tool_calls_per_step: int = Field(default=6, ge=1, le=20)
    redact_pii_in_observation: bool = True
    block_on_outreach: bool = False
    prompt_forbid_extra: str = Field(
        default="",
        description="Extra hard-forbid text appended to Prompt F_security",
    )

    @field_validator("kb_domains_allow")
    @classmethod
    def _kb_domains(cls, v: list[str]) -> list[str]:
        allowed = {"repair", "policy", "hr", "product", "channel"}
        out: list[str] = []
        for d in v:
            key = str(d).strip().lower()
            if not key:
                continue
            if key not in allowed:
                raise ValueError(f"Invalid kb domain: {key}; allowed {sorted(allowed)}")
            if key not in out:
                out.append(key)
        return out


class SkillConfig(BaseModel):
    """Canonical shape of skills/<id>/skill.yaml."""

    skill_id: str = Field(..., min_length=1)
    control_loop: Literal["act"] = Field(
        default="act",
        description="Platform control loop (Act Skills use act)",
    )
    department: str = Field(default="", description="Owning department narrative")
    goal: str = Field(..., min_length=1, description="One-line task goal")
    success_hint: str = Field(default="", description="Human-readable success criteria")
    success_when: str = Field(
        default="none",
        description="Machine-checkable success: wrote_ai_output|master_lookup|channel_lookup|none",
    )
    max_steps: int = Field(default=8, ge=1, le=32)
    tone: SkillTone
    allowed_tools: list[str] = Field(..., min_length=1)
    system_extra: str = Field(default="", description="Merged into Prompt [C] after goal")
    output_format: str = Field(default="", description="Merged into Prompt [E] final-answer format")
    security: SkillSecurity = Field(default_factory=SkillSecurity)

    @field_validator("allowed_tools")
    @classmethod
    def _uniq_tools(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for name in v:
            name = str(name).strip()
            if name and name not in out:
                out.append(name)
        if not out:
            raise ValueError("allowed_tools must not be empty")
        return out

    @field_validator("success_when")
    @classmethod
    def _success_when(cls, v: str) -> str:
        allowed = {
            "none",
            "wrote_ai_output",
            "master_lookup",
            "channel_lookup",
        }
        key = (v or "none").strip()
        if key not in allowed:
            raise ValueError(f"success_when must be one of {sorted(allowed)}")
        return key


# Prompt section order (do not reorder casually)
PROMPT_SECTION_ORDER: tuple[str, ...] = (
    "A_base",
    "B_tone",
    "C_goal",
    "C2_system_extra",
    "D_tools",
    "E_output",
    "F_security",
)


def skill_to_prompt_dict(cfg: SkillConfig) -> dict[str, Any]:
    """Serialize Skill config for prompt assembly."""
    return cfg.model_dump()

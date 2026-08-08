"""RAG Skill contract (separate from ReAct / Extraction)."""

from __future__ import annotations

from typing import Literal, Self

from pydantic import BaseModel, Field, field_validator, model_validator

KbDomainName = Literal["repair", "policy", "hr", "product", "channel"]


class RagTone(BaseModel):
    label: str = Field(..., min_length=1)
    style: str = Field(..., min_length=1)
    forbid: str = Field(default="")


class RagSecurity(BaseModel):
    prompt_forbid_extra: str = Field(default="")
    redact_pii: bool = True
    # ReAct domain ： search domain
    kb_domains_allow: list[str] = Field(default_factory=list)

    @field_validator("kb_domains_allow")
    @classmethod
    def _uniq_domains(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for name in v:
            name = str(name).strip()
            if name and name not in out:
                out.append(name)
        return out


class RagSkillConfig(BaseModel):
    """Skill config for retrieve → stuff → generate."""

    skill_id: str = Field(..., min_length=1)
    # （loader rag）； control_loop
    agent_type: Literal["rag"] = "rag"
    control_loop: Literal["retrieve"] = Field(
        default="retrieve",
        description="（Retrieve Skill retrieve）",
    )
    department: str = Field(default="")
    goal: str = Field(..., min_length=1)
    success_hint: str = Field(default="")
    tone: RagTone
    # domain （required ）；search domain
    kb_domains_allow: list[str] = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=10)
    max_context_chars: int = Field(default=2400, ge=400, le=8000)
    cite_required: bool = True
    allow_no_hit_answer: bool = True
    success_when: Literal["cited_answer", "none"] = "cited_answer"
    # shared （ ReAct ； catalog / document）
    allowed_tools: list[str] = Field(
        default_factory=lambda: [
            "search_kb",
            "get_kb_document",
            "list_kb_domains",
            "log_step",
        ]
    )
    system_extra: str = Field(default="")
    output_format: str = Field(default="")
    security: RagSecurity = Field(default_factory=RagSecurity)
    # optional： （R8）；
    write_ai_output: bool = False
    consumer_allow: list[str] = Field(default_factory=list)

    @field_validator("kb_domains_allow")
    @classmethod
    def _uniq_kb_domains(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for name in v:
            name = str(name).strip()
            if name and name not in out:
                out.append(name)
        if not out:
            raise ValueError("kb_domains_allow ")
        return out

    @field_validator("allowed_tools")
    @classmethod
    def _uniq_tools(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for name in v:
            name = str(name).strip()
            if name and name not in out:
                out.append(name)
        return out

    @field_validator("consumer_allow")
    @classmethod
    def _uniq_consumers(cls, v: list[str]) -> list[str]:
        out: list[str] = []
        for name in v:
            name = str(name).strip()
            if name and name not in out:
                out.append(name)
        return out

    @model_validator(mode="after")
    def _sync_security_domains(self) -> Self:
        if not self.security.kb_domains_allow:
            self.security = self.security.model_copy(
                update={"kb_domains_allow": list(self.kb_domains_allow)}
            )
        return self


RAG_PROMPT_SECTION_ORDER: tuple[str, ...] = (
    "A_base",
    "B_tone",
    "C_goal",
    "C2_system_extra",
    "D_retrieve_rules",
    "E_output",
    "F_security",
)
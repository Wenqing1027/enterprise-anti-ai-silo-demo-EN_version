"""Tool base types."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ToolContext:
    """Context for one call (permissions and audit limits)."""

    run_id: str | None = None
    skill_id: str | None = None
    agent_type: str | None = None
    # ， capability_catalog
    allowed_tools: list[str] | None = None
    # Skill.security.kb_domains_allow； thisdomain
    kb_domains_allow: list[str] | None = None


@dataclass
class ToolSpec:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., dict[str, Any]]
    readonly: bool = True
    # domain tag（master/commerce/service/…）； tool_class
    category: str = "general"
    required: list[str] = field(default_factory=list)
    # ：read | knowledge | write_govern
    tool_class: str = "read"


@dataclass
class ToolResult:
    ok: bool
    tool_name: str
    data: Any = None
    error: str | None = None
    error_code: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "tool_name": self.tool_name,
            "data": self.data,
            "error": self.error,
            "error_code": self.error_code,
        }


class ToolError(Exception):
    def __init__(self, message: str, code: str = "TOOL_ERROR") -> None:
        super().__init__(message)
        self.message = message
        self.code = code
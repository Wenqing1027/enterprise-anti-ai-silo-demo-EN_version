"""Pydantic base configuration."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class QingshuModel(BaseModel):
    """Qingshu Mobility unified data model base class."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=False,
    )

"""Data models · org (from standard-field-glossary)."""

from __future__ import annotations

from pydantic import Field

from shared.models.base import QingshuModel
from shared.models.enums import OrgLevel

class Org(QingshuModel):
    """Org · Org. Fields from standard field table."""

    org_id: str | None = Field(
        default=None,
        description="OrgID. Org unique ID",
        json_schema_extra={"example": "WZ-EAST"},
    )
    org_name: str | None = Field(
        default=None,
        description="OrgName. OrgDisplay name",
        json_schema_extra={"example": "War zone"},
    )
    org_level: OrgLevel | None = Field(
        default=None,
        description="OrgLayer. nation|warzone|subzone|block|dealer|outlet|store",
        json_schema_extra={"example": "warzone"},
    )
    parent_org_id: str | None = Field(
        default=None,
        description="OrgID. Org",
        json_schema_extra={"example": "NATION-CN"},
    )
    org_path: str | None = Field(
        default=None,
        description="Org. Layer",
        json_schema_extra={"example": "/ / / A"},
    )

class Region(QingshuModel):
    """Org · Region. Fields from standard field table."""

    province: str | None = Field(
        default=None,
        description=". -",
        json_schema_extra={"example": "demo"},
    )
    city: str | None = Field(
        default=None,
        description=". -",
        json_schema_extra={"example": "demo"},
    )
    county_code: str | None = Field(
        default=None,
        description="Field value.",
        json_schema_extra={"example": "320115"},
    )
    county_name: str | None = Field(
        default=None,
        description="Name.",
        json_schema_extra={"example": "demo"},
    )
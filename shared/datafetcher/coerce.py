"""dict Pydantic （ source ）。"""

from __future__ import annotations

from typing import TypeVar

from shared.models.base import QingshuModel

T = TypeVar("T", bound=QingshuModel)


def to_model(model_cls: type[T], row: dict) -> T:
    allowed = set(model_cls.model_fields)
    payload = {k: v for k, v in row.items() if k in allowed}
    return model_cls.model_validate(payload)
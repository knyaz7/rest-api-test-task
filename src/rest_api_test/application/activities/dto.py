from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class ActivityIn(BaseModel):
    name: str
    parent_id: UUID | None


class ActivityUpdate(ActivityIn):
    pass


class ActivityOut(ActivityIn):
    id: UUID
    children: list[ActivityOut] | None = None


ActivityOut.model_rebuild()

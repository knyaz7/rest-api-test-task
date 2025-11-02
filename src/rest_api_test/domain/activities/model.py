from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class Activity:
    id: UUID
    name: str
    parent_id: UUID | None
    children: list[Activity] | None = None

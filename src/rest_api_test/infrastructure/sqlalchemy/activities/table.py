from __future__ import annotations

from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rest_api_test.infrastructure.sqlalchemy.setup.base_model import Base


class ActivityOrm(Base):
    __tablename__ = "activities"

    name: Mapped[str]
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("activities.id", ondelete="SET NULL"), nullable=True
    )

    parent: Mapped[ActivityOrm | None] = relationship(
        back_populates="children", remote_side="ActivityOrm.id", passive_deletes=True
    )
    children: Mapped[list[ActivityOrm]] = relationship(
        back_populates="parent", lazy="selectin"
    )

    organizations: Mapped[list[OrganizationOrm]] = relationship(
        secondary="organizations_activities_map", back_populates="activities"
    )

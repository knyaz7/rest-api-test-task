from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rest_api_test.infrastructure.sqlalchemy.activities.table import ActivityOrm
from rest_api_test.infrastructure.sqlalchemy.buildings.table import BuildingOrm
from rest_api_test.infrastructure.sqlalchemy.phone_numbers.table import PhoneNumberOrm
from rest_api_test.infrastructure.sqlalchemy.setup.base_model import Base


class OrganizationOrm(Base):
    __tablename__ = "organizations"

    name: Mapped[str]

    building_id: Mapped[UUID] = mapped_column(
        ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False
    )

    building: Mapped[BuildingOrm] = relationship(
        back_populates="organizations", lazy="selectin"
    )

    activities: Mapped[list[ActivityOrm]] = relationship(
        secondary="organizations_activities_map",
        back_populates="organizations",
        lazy="selectin",
    )

    phone_numbers: Mapped[list[PhoneNumberOrm]] = relationship(
        secondary="organizations_pnumbers_map",
        back_populates="organizations",
        lazy="selectin",
    )

from decimal import Decimal

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from rest_api_test.infrastructure.sqlalchemy.setup.base_model import Base


class BuildingOrm(Base):
    __tablename__ = "buildings"

    address: Mapped[str]

    latitude: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)

    organizations: Mapped[list["OrganizationOrm"]] = relationship(
        back_populates="building", cascade="all, delete-orphan", passive_deletes=True
    )

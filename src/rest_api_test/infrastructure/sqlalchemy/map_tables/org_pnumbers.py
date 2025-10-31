from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from rest_api_test.infrastructure.sqlalchemy.setup.base_model import Base


class OrganizationPNumbersMapOrm(Base):
    __tablename__ = "organizations_pnumbers_map"

    organization_id: Mapped[UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True
    )
    phone_number_id: Mapped[UUID] = mapped_column(
        ForeignKey("phone_numbers.id", ondelete="CASCADE"), primary_key=True
    )

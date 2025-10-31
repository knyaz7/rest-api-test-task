from sqlalchemy.orm import Mapped, relationship

from rest_api_test.infrastructure.sqlalchemy.setup.base_model import Base


class PhoneNumberOrm(Base):
    __tablename__ = "phone_numbers"

    phone_number: Mapped[str]

    organizations: Mapped[list["OrganizationOrm"]] = relationship(
        secondary="organizations_pnumbers_map", back_populates="phone_numbers"
    )

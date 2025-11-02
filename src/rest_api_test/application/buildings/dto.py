from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, field_validator


class BuildingIn(BaseModel):
    address: str
    latitude: Decimal
    longitude: Decimal

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: Decimal) -> Decimal:
        if not (-90 <= v <= 90):
            raise ValueError("Latitude must be between -90 and 90 degrees")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: Decimal) -> Decimal:
        if not (-180 <= v <= 180):
            raise ValueError("Longitude must be between -180 and 180 degrees")
        return v


class BuildingUpdate(BuildingIn):
    pass


class BuildingOut(BuildingIn):
    id: UUID

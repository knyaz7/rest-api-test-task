from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, confloat, conint, model_validator


class GeoFilterKindEnum(StrEnum):
    RADIUS = "radius"
    BBOX = "bbox"


class GeoFilterBase(BaseModel):
    kind: GeoFilterKindEnum


class GeoRadius(GeoFilterBase):
    kind = GeoFilterKindEnum.RADIUS
    lat: Annotated[float, confloat(ge=-90, le=90)]
    lon: Annotated[float, confloat(ge=-180, le=180)]
    radius_m: Annotated[float, conint(gt=0, le=100_000)]


class GeoBBox(GeoFilterBase):
    kind = GeoFilterKindEnum.BBOX
    lat_min: Annotated[float, confloat(ge=-90, le=90)]
    lat_max: Annotated[float, confloat(ge=-90, le=90)]
    lon_min: Annotated[float, confloat(ge=-180, le=180)]
    lon_max: Annotated[float, confloat(ge=-180, le=180)]

    @model_validator(mode="after")
    def _check_ranges(self):
        if not (self.lat_min < self.lat_max and self.lon_min < self.lon_max):
            raise ValueError("bbox: lat_min < lat_max и lon_min < lon_max обязательны")
        return self


GeoFilter = GeoRadius | GeoBBox | None


class OrganizationsQuery(BaseModel):
    name: str | None = None
    building_id: UUID | None = None
    activity_id: UUID | None = None
    geo: GeoFilter | None = None

    @model_validator(mode="after")
    def _validate_logic(self):
        # гео и building_id взаимоисключающие (иначе двусмысленно)
        if self.geo is not None and self.building_id is not None:
            raise ValueError("Нельзя одновременно фильтровать по building_id и geo")

        return self


class OrganizationOut(BaseModel):
    id: UUID
    name: str
    phone_numbers: list[PhoneNumber]
    activities: list[Activity]
    building_id: UUID

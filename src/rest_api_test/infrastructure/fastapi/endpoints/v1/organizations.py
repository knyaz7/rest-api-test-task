from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_cache.decorator import cache

from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.organizations.dto import (
    GeoBBox,
    GeoFilterKindEnum,
    GeoRadius,
    OrganizationIn,
    OrganizationOut,
    OrganizationsQuery,
    OrganizationUpdate,
)
from rest_api_test.application.organizations.service import OrganizationService
from rest_api_test.infrastructure.di.container import Container
from rest_api_test.infrastructure.fastapi.dependencies.pagination import get_pagination

organizations_router = APIRouter(prefix="/organizations", tags=["Organizations"])


async def parse_orgs_query_flat(
    name: str | None = None,
    building_id: UUID | None = None,
    activity_id: UUID | None = None,
    geo_kind: GeoFilterKindEnum | None = Query(None),
    lat: float | None = Query(None, ge=-90, le=90),
    lon: float | None = Query(None, ge=-180, le=180),
    radius_m: int | None = Query(None, gt=0, le=100_000),
    lat_min: float | None = Query(None, ge=-90, le=90),
    lat_max: float | None = Query(None, ge=-90, le=90),
    lon_min: float | None = Query(None, ge=-180, le=180),
    lon_max: float | None = Query(None, ge=-180, le=180),
) -> OrganizationsQuery:
    geo_obj = None
    if geo_kind == GeoFilterKindEnum.RADIUS:
        if lat is None or lon is None or radius_m is None:
            raise HTTPException(422, "lat/lon/radius_m required for radius")
        geo_obj = GeoRadius(lat=lat, lon=lon, radius_m=radius_m)
    elif geo_kind == GeoFilterKindEnum.BBOX:
        if None in (lat_min, lat_max, lon_min, lon_max):
            raise HTTPException(
                422, "lat_min/lat_max/lon_min/lon_max required for bbox"
            )
        geo_obj = GeoBBox(
            lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max
        )

    return OrganizationsQuery(
        name=name, building_id=building_id, activity_id=activity_id, geo=geo_obj
    )


@organizations_router.get("/", response_model=list[OrganizationOut])
@cache(10)
@inject
async def get_organizations(
    orgs_query: Annotated[OrganizationsQuery, Depends(parse_orgs_query_flat)],
    orgs_service: Annotated[
        OrganizationService, Depends(Provide[Container.orgs_service])
    ],
    pagination: Annotated[Pagination, Depends(get_pagination)],
):
    return await orgs_service.get_all(pagination, orgs_query)


@organizations_router.get("/{org_id}", response_model=OrganizationOut)
@cache(10)
@inject
async def get_organization(
    org_id: UUID,
    orgs_service: Annotated[
        OrganizationService, Depends(Provide[Container.orgs_service])
    ],
):
    return await orgs_service.get_by_id(org_id)


@organizations_router.post("/", response_model=OrganizationOut)
@inject
async def create_organization(
    org_payload: OrganizationIn,
    orgs_service: Annotated[
        OrganizationService, Depends(Provide[Container.orgs_service])
    ],
):
    return await orgs_service.create(org_payload)


@organizations_router.post("/activity", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def assign_activity(
    organization_id: UUID,
    activity_id: UUID,
    orgs_service: Annotated[
        OrganizationService, Depends(Provide[Container.orgs_service])
    ],
):
    await orgs_service.assign_activity(organization_id, activity_id)


@organizations_router.delete("/activity", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def unassign_activity(
    organization_id: UUID,
    activity_id: UUID,
    orgs_service: Annotated[
        OrganizationService, Depends(Provide[Container.orgs_service])
    ],
):
    await orgs_service.unassign_activity(organization_id, activity_id)


@organizations_router.post("/phone-number", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def assign_phone_number(
    organization_id: UUID,
    phone_number_id: UUID,
    orgs_service: Annotated[
        OrganizationService, Depends(Provide[Container.orgs_service])
    ],
):
    await orgs_service.assign_phone_number(organization_id, phone_number_id)


@organizations_router.delete("/phone-number", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def unassign_phone_number(
    organization_id: UUID,
    phone_number_id: UUID,
    orgs_service: Annotated[
        OrganizationService, Depends(Provide[Container.orgs_service])
    ],
):
    await orgs_service.unassign_phone_number(organization_id, phone_number_id)


@organizations_router.put("/{org_id}", response_model=OrganizationOut)
@inject
async def update_organization(
    org_id: UUID,
    org_payload: OrganizationUpdate,
    orgs_service: Annotated[
        OrganizationService, Depends(Provide[Container.orgs_service])
    ],
):
    return await orgs_service.update(org_id, org_payload)


@organizations_router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_organization(
    org_id: UUID,
    orgs_service: Annotated[
        OrganizationService, Depends(Provide[Container.orgs_service])
    ],
):
    await orgs_service.delete(org_id)

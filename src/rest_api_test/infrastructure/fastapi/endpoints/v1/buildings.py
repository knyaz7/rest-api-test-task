from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from rest_api_test.application.buildings.dto import (
    BuildingIn,
    BuildingOut,
    BuildingUpdate,
)
from rest_api_test.application.buildings.service import BuildingService
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.infrastructure.di.container import Container
from rest_api_test.infrastructure.fastapi.dependencies.pagination import get_pagination

buildings_router = APIRouter(prefix="/buildings", tags=["Buildings"])


@buildings_router.get("/", response_model=list[BuildingOut])
@cache(10)
@inject
async def get_buildings(
    pagination: Annotated[Pagination, Depends(get_pagination)],
    buildings_service: Annotated[
        BuildingService, Depends(Provide[Container.buildings_service])
    ],
) -> list[BuildingOut]:
    return await buildings_service.get_all(pagination)


@buildings_router.get("/{building_id}", response_model=BuildingOut)
@cache(10)
@inject
async def get_building(
    building_id: UUID,
    buildings_service: Annotated[
        BuildingService, Depends(Provide[Container.buildings_service])
    ],
) -> BuildingOut:
    return await buildings_service.get_by_id(building_id)


@buildings_router.post(
    "/", response_model=BuildingOut, status_code=status.HTTP_201_CREATED
)
@inject
async def create_building(
    payload: BuildingIn,
    buildings_service: Annotated[
        BuildingService, Depends(Provide[Container.buildings_service])
    ],
) -> BuildingOut:
    return await buildings_service.create(payload)


@buildings_router.put("/{building_id}", response_model=BuildingOut)
@inject
async def update_building(
    building_id: UUID,
    payload: BuildingUpdate,
    buildings_service: Annotated[
        BuildingService, Depends(Provide[Container.buildings_service])
    ],
) -> BuildingOut:
    return await buildings_service.update(building_id, payload)


@buildings_router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_building(
    building_id: UUID,
    buildings_service: Annotated[
        BuildingService, Depends(Provide[Container.buildings_service])
    ],
) -> None:
    await buildings_service.delete(building_id)

from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from rest_api_test.application.activities.dto import (
    ActivityIn,
    ActivityOut,
    ActivityUpdate,
)
from rest_api_test.application.activities.service import ActivityService
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.infrastructure.di.container import Container
from rest_api_test.infrastructure.fastapi.dependencies.pagination import get_pagination

activities_router = APIRouter(prefix="/activities", tags=["Activities"])


@activities_router.get("/", response_model=list[ActivityOut])
@cache(10)
@inject
async def get_activities(
    pagination: Annotated[Pagination, Depends(get_pagination)],
    activities_service: Annotated[
        ActivityService, Depends(Provide[Container.activities_service])
    ],
) -> list[ActivityOut]:
    return await activities_service.get_all(pagination)


@activities_router.get("/{activity_id}", response_model=ActivityOut)
@cache(10)
@inject
async def get_activity(
    activity_id: UUID,
    activities_service: Annotated[
        ActivityService, Depends(Provide[Container.activities_service])
    ],
) -> ActivityOut:
    return await activities_service.get_by_id(activity_id)


@activities_router.post(
    "/", response_model=ActivityOut, status_code=status.HTTP_201_CREATED
)
@inject
async def create_activity(
    payload: ActivityIn,
    activities_service: Annotated[
        ActivityService, Depends(Provide[Container.activities_service])
    ],
) -> ActivityOut:
    return await activities_service.create(payload)


@activities_router.put("/{activity_id}", response_model=ActivityOut)
@inject
async def update_activity(
    activity_id: UUID,
    payload: ActivityUpdate,
    activities_service: Annotated[
        ActivityService, Depends(Provide[Container.activities_service])
    ],
) -> ActivityOut:
    return await activities_service.update(activity_id, payload)


@activities_router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_activity(
    activity_id: UUID,
    activities_service: Annotated[
        ActivityService, Depends(Provide[Container.activities_service])
    ],
) -> None:
    await activities_service.delete(activity_id)

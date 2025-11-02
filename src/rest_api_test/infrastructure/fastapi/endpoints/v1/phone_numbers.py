from typing import Annotated
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.phone_numbers.dto import (
    PhoneNumberIn,
    PhoneNumberOut,
    PhoneNumberUpdate,
)
from rest_api_test.application.phone_numbers.service import PhoneNumberService
from rest_api_test.infrastructure.di.container import Container
from rest_api_test.infrastructure.fastapi.dependencies.pagination import get_pagination

phone_numbers_router = APIRouter(prefix="/phone-numbers", tags=["Phone numbers"])


@phone_numbers_router.get("/", response_model=list[PhoneNumberOut])
@cache(10)
@inject
async def get_phone_numbers(
    pagination: Annotated[Pagination, Depends(get_pagination)],
    phone_numbers_service: Annotated[
        PhoneNumberService, Depends(Provide[Container.phone_numbers_service])
    ],
) -> list[PhoneNumberOut]:
    return await phone_numbers_service.get_all(pagination)


@phone_numbers_router.get("/{phone_id}", response_model=PhoneNumberOut)
@cache(10)
@inject
async def get_phone_number(
    phone_id: UUID,
    phone_numbers_service: Annotated[
        PhoneNumberService, Depends(Provide[Container.phone_numbers_service])
    ],
) -> PhoneNumberOut:
    return await phone_numbers_service.get_by_id(phone_id)


@phone_numbers_router.post(
    "/", response_model=PhoneNumberOut, status_code=status.HTTP_201_CREATED
)
@inject
async def create_phone_number(
    payload: PhoneNumberIn,
    phone_numbers_service: Annotated[
        PhoneNumberService, Depends(Provide[Container.phone_numbers_service])
    ],
) -> PhoneNumberOut:
    return await phone_numbers_service.create(payload)


@phone_numbers_router.put("/{phone_id}", response_model=PhoneNumberOut)
@inject
async def update_phone_number(
    phone_id: UUID,
    payload: PhoneNumberUpdate,
    phone_numbers_service: Annotated[
        PhoneNumberService, Depends(Provide[Container.phone_numbers_service])
    ],
) -> PhoneNumberOut:
    return await phone_numbers_service.update(phone_id, payload)


@phone_numbers_router.delete("/{phone_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_phone_number(
    phone_id: UUID,
    phone_numbers_service: Annotated[
        PhoneNumberService, Depends(Provide[Container.phone_numbers_service])
    ],
) -> None:
    await phone_numbers_service.delete(phone_id)

from uuid import UUID

from rest_api_test.application.exceptions.app_error import NotFound
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.interfaces.common.uow import UnitOfWork
from rest_api_test.application.phone_numbers.dto import (
    PhoneNumberIn,
    PhoneNumberOut,
    PhoneNumberUpdate,
)
from rest_api_test.application.phone_numbers.repo import PhoneNumberRepository
from rest_api_test.domain.phone_numbers.table import PhoneNumber


class PhoneNumberService:
    def __init__(self, uow: UnitOfWork, repo: PhoneNumberRepository):
        self.uow = uow
        self.repo = repo

    async def get_all(self, pagination: Pagination) -> list[PhoneNumberOut]:
        async with self.uow:
            phone_numbers = await self.repo.get_all(pagination)
        return [
            PhoneNumberOut.model_validate(number, from_attributes=True)
            for number in phone_numbers
        ]

    async def get_by_id(self, phone_id: UUID) -> PhoneNumberOut:
        async with self.uow:
            phone_number = await self.repo.get_by_id(phone_id)
        if not phone_number:
            raise NotFound.domain_entity(PhoneNumber, phone_id)
        return PhoneNumberOut.model_validate(phone_number, from_attributes=True)

    async def create(self, payload: PhoneNumberIn) -> PhoneNumberOut:
        async with self.uow as uow:
            phone_number = await self.repo.create(payload)
            await uow.commit()
        return PhoneNumberOut.model_validate(phone_number, from_attributes=True)

    async def update(
        self, phone_id: UUID, payload: PhoneNumberUpdate
    ) -> PhoneNumberOut:
        async with self.uow as uow:
            phone_number = await self.repo.update(phone_id, payload)
            await uow.commit()
        return PhoneNumberOut.model_validate(phone_number, from_attributes=True)

    async def delete(self, phone_id: UUID) -> None:
        async with self.uow as uow:
            await self.repo.delete_by_id(phone_id)
            await uow.commit()

from uuid import UUID

from rest_api_test.application.exceptions.app_error import NotFound
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.phone_numbers.dto import PhoneNumberIn, PhoneNumberUpdate
from rest_api_test.application.phone_numbers.repo import PhoneNumberRepository
from rest_api_test.domain.phone_numbers.table import PhoneNumber
from rest_api_test.infrastructure.sqlalchemy.phone_numbers.mapper import to_domain
from rest_api_test.infrastructure.sqlalchemy.phone_numbers.table import PhoneNumberOrm
from rest_api_test.infrastructure.sqlalchemy.setup.base_repo import AlchemyRepo


class AlchemyPhoneNumberRepo(PhoneNumberRepository, AlchemyRepo[PhoneNumberOrm]):
    model = PhoneNumberOrm

    async def get_all(self, pagination: Pagination) -> list[PhoneNumber]:
        rows = await self._get_all(pagination)
        return [to_domain(row) for row in rows]

    async def get_by_id(self, pn_id: UUID) -> PhoneNumber | None:
        entity = await self._get_by_id(pn_id)
        if entity:
            return to_domain(entity)
        return None

    async def create(self, data: PhoneNumberIn) -> PhoneNumber:
        entity = await self._create(data.model_dump())
        return to_domain(entity)

    async def update(self, pn_id: UUID, data: PhoneNumberUpdate) -> PhoneNumber:
        entity = await self._update_by_id(pn_id, data.model_dump())
        return to_domain(entity)

    async def delete_by_id(self, pn_id: UUID) -> PhoneNumber:
        entity = await self._get_by_id(pn_id)
        if entity is None:
            raise NotFound.domain_entity(PhoneNumber, pn_id)
        domain = to_domain(entity)
        await self._delete(pn_id)
        return domain

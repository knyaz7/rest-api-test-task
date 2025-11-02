from uuid import UUID

from rest_api_test.application.buildings.dto import BuildingIn, BuildingUpdate
from rest_api_test.application.buildings.repo import BuildingRepository
from rest_api_test.application.exceptions.app_error import NotFound
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.domain.buildings.model import Building
from rest_api_test.infrastructure.sqlalchemy.buildings.mapper import to_domain
from rest_api_test.infrastructure.sqlalchemy.buildings.table import BuildingOrm
from rest_api_test.infrastructure.sqlalchemy.setup.base_repo import AlchemyRepo


class AlchemyBuildingRepo(BuildingRepository, AlchemyRepo[BuildingOrm]):
    model = BuildingOrm

    async def get_all(self, pagination: Pagination) -> list[Building]:
        rows = await self._get_all(pagination)
        return [to_domain(row) for row in rows]

    async def get_by_id(self, bld_id: UUID) -> Building | None:
        entity = await self._get_by_id(bld_id)
        if entity:
            return to_domain(entity)
        return None

    async def create(self, data: BuildingIn) -> Building:
        entity = await self._create(data.model_dump())
        return to_domain(entity)

    async def update(self, bld_id: UUID, data: BuildingUpdate) -> Building:
        entity = await self._update_by_id(bld_id, data.model_dump())
        return to_domain(entity)

    async def delete_by_id(self, bld_id: UUID) -> Building:
        entity = await self._get_by_id(bld_id)
        if entity is None:
            raise NotFound.domain_entity(Building, bld_id)
        domain = to_domain(entity)
        await self._delete(bld_id)
        return domain

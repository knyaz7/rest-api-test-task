from uuid import UUID

from rest_api_test.application.buildings.dto import (
    BuildingIn,
    BuildingOut,
    BuildingUpdate,
)
from rest_api_test.application.buildings.repo import BuildingRepository
from rest_api_test.application.exceptions.app_error import NotFound
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.interfaces.common.uow import UnitOfWork
from rest_api_test.domain.buildings.model import Building


class BuildingService:
    def __init__(self, uow: UnitOfWork, repo: BuildingRepository):
        self.uow = uow
        self.repo = repo

    async def get_all(self, pagination: Pagination) -> list[BuildingOut]:
        async with self.uow:
            buildings = await self.repo.get_all(pagination)
        return [
            BuildingOut.model_validate(bld, from_attributes=True) for bld in buildings
        ]

    async def get_by_id(self, building_id: UUID) -> BuildingOut:
        async with self.uow:
            building = await self.repo.get_by_id(building_id)
        if not building:
            raise NotFound.domain_entity(Building, building_id)
        return BuildingOut.model_validate(building, from_attributes=True)

    async def create(self, payload: BuildingIn) -> BuildingOut:
        async with self.uow as uow:
            building = await self.repo.create(payload)
            await uow.commit()
        return BuildingOut.model_validate(building, from_attributes=True)

    async def update(self, building_id: UUID, payload: BuildingUpdate) -> BuildingOut:
        async with self.uow as uow:
            building = await self.repo.update(building_id, payload)
            await uow.commit()
        return BuildingOut.model_validate(building, from_attributes=True)

    async def delete(self, building_id: UUID) -> None:
        async with self.uow as uow:
            await self.repo.delete_by_id(building_id)
            await uow.commit()

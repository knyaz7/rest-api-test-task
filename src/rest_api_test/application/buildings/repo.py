from abc import ABC, abstractmethod
from uuid import UUID

from rest_api_test.application.buildings.dto import BuildingIn, BuildingUpdate
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.domain.buildings.model import Building


class BuildingRepository(ABC):
    @abstractmethod
    async def get_all(self, pagination: Pagination) -> list[Building]: ...

    @abstractmethod
    async def get_by_id(self, bld_id: UUID) -> Building | None: ...

    @abstractmethod
    async def create(self, data: BuildingIn) -> Building: ...

    @abstractmethod
    async def update(self, bld_id: UUID, data: BuildingUpdate) -> Building: ...

    @abstractmethod
    async def delete_by_id(self, bld_id: UUID) -> Building: ...

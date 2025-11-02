from abc import ABC, abstractmethod
from uuid import UUID

from rest_api_test.application.activities.dto import ActivityIn, ActivityUpdate
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.domain.activities.model import Activity


class ActivityRepository(ABC):
    @abstractmethod
    async def get_all(self, pagination: Pagination) -> list[Activity]: ...

    @abstractmethod
    async def get_by_id(self, act_id: UUID) -> Activity | None: ...

    @abstractmethod
    async def create(self, data: ActivityIn) -> Activity: ...

    @abstractmethod
    async def update(self, act_id: UUID, data: ActivityUpdate) -> Activity: ...

    @abstractmethod
    async def delete_by_id(self, act_id: UUID) -> Activity: ...

from abc import ABC, abstractmethod
from uuid import UUID

from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.organizations.dto import (
    GeoFilter,
    OrganizationIn,
    OrganizationUpdate,
)
from rest_api_test.domain.organizations.model import Organization


class OrganizationRepository(ABC):
    @abstractmethod
    async def get_all(
        self,
        pagination: Pagination | None = None,
        name: str | None = None,
        building_id: UUID | None = None,
        activity_id: UUID | None = None,
        geo: GeoFilter | None = None,
    ) -> list[Organization]: ...

    @abstractmethod
    async def get_by_id(self, org_id: UUID) -> Organization | None: ...

    @abstractmethod
    async def create(self, payload: OrganizationIn) -> Organization: ...

    @abstractmethod
    async def assign_phone_numbers(self, org_id: UUID, ids: list[UUID]) -> None: ...

    @abstractmethod
    async def unassign_phone_numbers(self, org_id: UUID, ids: list[UUID]) -> None: ...

    @abstractmethod
    async def assign_activities(self, org_id: UUID, ids: list[UUID]) -> None: ...

    @abstractmethod
    async def unassign_activities(self, org_id: UUID, ids: list[UUID]) -> None: ...

    @abstractmethod
    async def update_by_id(
        self, org_id: UUID, payload: OrganizationUpdate
    ) -> Organization: ...

    @abstractmethod
    async def delete_by_id(self, org_id: UUID) -> None: ...

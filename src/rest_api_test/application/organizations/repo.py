from uuid import UUID

from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.organizations.dto import GeoFilter
from rest_api_test.domain.organizations.model import Organization


class OrganizationRepository:
    async def get_all(
        self,
        pagination: Pagination | None = None,
        name: str | None = None,
        building_id: UUID | None = None,
        activity_id: UUID | None = None,
        geo: GeoFilter | None = None,
    ) -> list[Organization]: ...

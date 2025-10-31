from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.interfaces.common.uow import UnitOfWork
from rest_api_test.application.organizations.dto import (
    OrganizationOut,
    OrganizationsQuery,
)
from rest_api_test.application.organizations.repo import OrganizationRepository


class OrganizationService:
    def __init__(self, uow: UnitOfWork, orgs_repo: OrganizationRepository):
        self.uow = uow
        self.orgs_repo = orgs_repo

    async def get_all(
        self, pagination: Pagination, query: OrganizationsQuery
    ) -> list[OrganizationOut]:
        async with self.uow:
            orgs = await self.orgs_repo.get_all(
                pagination=pagination,
                name=query.name,
                building_id=query.building_id,
                activity_id=query.activity_id,
                geo=query.geo,
            )
        return [OrganizationOut.model_validate(o, from_attributes=True) for o in orgs]

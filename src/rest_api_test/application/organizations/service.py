from uuid import UUID

from rest_api_test.application.activities.repo import ActivityRepository
from rest_api_test.application.buildings.repo import BuildingRepository
from rest_api_test.application.exceptions.app_error import NotFound
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.interfaces.common.uow import UnitOfWork
from rest_api_test.application.organizations.dto import (
    OrganizationIn,
    OrganizationOut,
    OrganizationsQuery,
    OrganizationUpdate,
)
from rest_api_test.application.organizations.repo import OrganizationRepository
from rest_api_test.application.phone_numbers.repo import PhoneNumberRepository
from rest_api_test.domain.activities.model import Activity
from rest_api_test.domain.buildings.model import Building
from rest_api_test.domain.organizations.model import Organization
from rest_api_test.domain.phone_numbers.table import PhoneNumber


class OrganizationService:
    def __init__(
        self,
        uow: UnitOfWork,
        orgs_repo: OrganizationRepository,
        build_repo: BuildingRepository,
        activity_repo: ActivityRepository,
        phone_repo: PhoneNumberRepository,
    ):
        self.uow = uow
        self.orgs_repo = orgs_repo
        self.build_repo = build_repo
        self.activity_repo = activity_repo
        self.phone_repo = phone_repo

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

    async def get_by_id(self, org_id: UUID) -> OrganizationOut:
        async with self.uow:
            org = await self.orgs_repo.get_by_id(org_id)
        if not org:
            raise NotFound.domain_entity(Organization, org_id)
        return OrganizationOut.model_validate(org, from_attributes=True)

    async def create(self, payload: OrganizationIn) -> OrganizationOut:
        async with self.uow as uow:
            building = await self.build_repo.get_by_id(payload.building_id)
            if not building:
                raise NotFound.domain_entity(Building, payload.building_id)
            org = await self.orgs_repo.create(payload)
            await uow.commit()
        return OrganizationOut.model_validate(org, from_attributes=True)

    async def assign_activity(self, org_id: UUID, activity_id: UUID) -> None:
        async with self.uow as uow:
            org = await self.orgs_repo.get_by_id(org_id)
            if not org:
                raise NotFound.domain_entity(Organization, org_id)

            activity = await self.activity_repo.get_by_id(activity_id)
            if not activity:
                raise NotFound.domain_entity(Activity, activity_id)
            await self.orgs_repo.assign_activities(org_id, [activity_id])
            await uow.commit()

    async def unassign_activity(self, org_id: UUID, activity_id: UUID) -> None:
        async with self.uow as uow:
            org = await self.orgs_repo.get_by_id(org_id)
            if not org:
                raise NotFound.domain_entity(Organization, org_id)

            activity = await self.activity_repo.get_by_id(activity_id)
            if not activity:
                raise NotFound.domain_entity(Activity, activity_id)
            await self.orgs_repo.unassign_activities(org_id, [activity_id])
            await uow.commit()

    async def assign_phone_number(self, org_id: UUID, phone_id: UUID) -> None:
        async with self.uow as uow:
            org = await self.orgs_repo.get_by_id(org_id)
            if not org:
                raise NotFound.domain_entity(Organization, org_id)

            phone = await self.phone_repo.get_by_id(phone_id)
            if not phone:
                raise NotFound.domain_entity(PhoneNumber, phone_id)

            await self.orgs_repo.assign_phone_numbers(org_id, [phone_id])
            await uow.commit()

    async def unassign_phone_number(self, org_id: UUID, phone_id: UUID) -> None:
        async with self.uow as uow:
            org = await self.orgs_repo.get_by_id(org_id)
            if not org:
                raise NotFound.domain_entity(Organization, org_id)

            phone = await self.phone_repo.get_by_id(phone_id)
            if not phone:
                raise NotFound.domain_entity(PhoneNumber, phone_id)

            await self.orgs_repo.unassign_phone_numbers(org_id, [phone_id])
            await uow.commit()

    async def update(
        self, org_id: UUID, payload: OrganizationUpdate
    ) -> OrganizationOut:
        async with self.uow as uow:
            building = await self.build_repo.get_by_id(payload.building_id)
            if not building:
                raise NotFound.domain_entity(Building, payload.building_id)
            org = await self.orgs_repo.update_by_id(org_id, payload)
            await uow.commit()
        return OrganizationOut.model_validate(org, from_attributes=True)

    async def delete(self, org_id: UUID) -> None:
        async with self.uow as uow:
            await self.orgs_repo.delete_by_id(org_id)
            await uow.commit()

from decimal import Decimal
from uuid import UUID

from rest_api_test.application.activities.dto import ActivityIn
from rest_api_test.application.activities.repo import ActivityRepository
from rest_api_test.application.buildings.dto import BuildingIn
from rest_api_test.application.buildings.repo import BuildingRepository
from rest_api_test.application.interfaces.common.uow import UnitOfWork
from rest_api_test.application.organizations.dto import OrganizationIn
from rest_api_test.application.organizations.repo import OrganizationRepository
from rest_api_test.application.phone_numbers.dto import PhoneNumberIn
from rest_api_test.application.phone_numbers.repo import PhoneNumberRepository
from rest_api_test.utils.logging.logger import get_logger

logger = get_logger(__name__)


class DataFiller:
    def __init__(
        self,
        org_repo: OrganizationRepository,
        activity_repo: ActivityRepository,
        pn_repo: PhoneNumberRepository,
        building_repo: BuildingRepository,
        uow: UnitOfWork,
    ):
        self.org_repo = org_repo
        self.activity_repo = activity_repo
        self.pn_repo = pn_repo
        self.building_repo = building_repo
        self.uow = uow

    async def fill_database(self):
        async with self.uow:
            activity_ids = await self._fill_activities()
            phone_numbers_ids = await self._fill_phone_numbers()
            await self._fill_organizations(activity_ids, phone_numbers_ids)
            await self.uow.commit()

    async def _fill_activities(self) -> list[UUID]:
        """Returns root activities uuids"""
        food_act_payload = ActivityIn(name="Food", parent_id=None)
        food_activity = await self.activity_repo.create(food_act_payload)

        meat_act_payload = ActivityIn(name="Meat", parent_id=food_activity.id)
        await self.activity_repo.create(meat_act_payload)

        dairy_act_payload = ActivityIn(name="Milk", parent_id=food_activity.id)
        await self.activity_repo.create(dairy_act_payload)

        cars_act_payload = ActivityIn(name="Cards", parent_id=None)
        cars_activity = await self.activity_repo.create(cars_act_payload)

        trucks_act_payload = ActivityIn(name="Trucks", parent_id=cars_activity.id)
        await self.activity_repo.create(trucks_act_payload)

        light_cars_payload = ActivityIn(name="Light cars", parent_id=cars_activity.id)
        light_cars_activity = await self.activity_repo.create(light_cars_payload)

        parts_payload = ActivityIn(name="Parts", parent_id=light_cars_activity.id)
        await self.activity_repo.create(parts_payload)

        accessories_payload = ActivityIn(
            name="Accessories", parent_id=light_cars_activity.id
        )
        await self.activity_repo.create(accessories_payload)
        return [food_activity.id, cars_activity.id]

    async def _fill_phone_numbers(self) -> list[UUID]:
        first_number_payload = PhoneNumberIn(phone_number="+78005553535")
        second_number_payload = PhoneNumberIn(phone_number="+78005553536")
        first_number = await self.pn_repo.create(first_number_payload)
        second_number = await self.pn_repo.create(second_number_payload)
        return [first_number.id, second_number.id]

    async def _fill_organizations(self, activities_ids: list[UUID], pn_ids: list[UUID]):
        building_payload = BuildingIn(
            address="Moscow, Lenin str. 3",
            latitude=Decimal("55.7558"),
            longitude=Decimal("37.6176"),
        )
        building = await self.building_repo.create(building_payload)

        org_payload = OrganizationIn(name="Horns and hooves", building_id=building.id)
        organization = await self.org_repo.create(org_payload)

        await self.org_repo.assign_activities(organization.id, activities_ids)
        await self.org_repo.assign_phone_numbers(organization.id, pn_ids)

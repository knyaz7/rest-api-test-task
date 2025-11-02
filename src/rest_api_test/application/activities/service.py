from uuid import UUID

from rest_api_test.application.activities.dto import (
    ActivityIn,
    ActivityOut,
    ActivityUpdate,
)
from rest_api_test.application.activities.repo import ActivityRepository
from rest_api_test.application.exceptions.app_error import NotFound
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.interfaces.common.uow import UnitOfWork
from rest_api_test.domain.activities.model import Activity


class ActivityService:
    def __init__(self, uow: UnitOfWork, repo: ActivityRepository):
        self.uow = uow
        self.repo = repo

    async def get_all(self, pagination: Pagination) -> list[ActivityOut]:
        async with self.uow:
            activities = await self.repo.get_all(pagination)
        return [
            ActivityOut.model_validate(activity, from_attributes=True)
            for activity in activities
        ]

    async def get_by_id(self, activity_id: UUID) -> ActivityOut:
        async with self.uow:
            activity = await self.repo.get_by_id(activity_id)
        if not activity:
            raise NotFound.domain_entity(Activity, activity_id)
        return ActivityOut.model_validate(activity, from_attributes=True)

    async def create(self, payload: ActivityIn) -> ActivityOut:
        async with self.uow as uow:
            activity = await self.repo.create(payload)
            await uow.commit()
        return ActivityOut.model_validate(activity, from_attributes=True)

    async def update(self, activity_id: UUID, payload: ActivityUpdate) -> ActivityOut:
        async with self.uow as uow:
            activity = await self.repo.update(activity_id, payload)
            await uow.commit()
        return ActivityOut.model_validate(activity, from_attributes=True)

    async def delete(self, activity_id: UUID) -> None:
        async with self.uow as uow:
            await self.repo.delete_by_id(activity_id)
            await uow.commit()

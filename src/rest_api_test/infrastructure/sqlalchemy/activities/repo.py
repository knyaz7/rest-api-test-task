from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from rest_api_test.application.activities.dto import ActivityIn, ActivityUpdate
from rest_api_test.application.activities.repo import ActivityRepository
from rest_api_test.application.exceptions.app_error import NotFound
from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.domain.activities.model import Activity
from rest_api_test.infrastructure.sqlalchemy.activities.mapper import to_domain
from rest_api_test.infrastructure.sqlalchemy.activities.table import ActivityOrm
from rest_api_test.infrastructure.sqlalchemy.setup.base_repo import AlchemyRepo
from rest_api_test.utils.config.settings import get_settings

settings = get_settings()


class AlchemyActivityRepo(ActivityRepository, AlchemyRepo[ActivityOrm]):
    model = ActivityOrm

    async def get_all(self, pagination: Pagination) -> list[Activity]:
        query = select(ActivityOrm).options(self._tree_loader())
        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)
        res = await self._session.execute(query)
        rows = res.scalars().all()
        return [to_domain(row, max_depth=settings.activities_depth) for row in rows]

    async def get_by_id(self, act_id: UUID) -> Activity | None:
        query = (
            select(ActivityOrm)
            .where(ActivityOrm.id == act_id)
            .options(self._tree_loader())
        )
        res = await self._session.execute(query)
        entity = res.scalar_one_or_none()
        if entity:
            return to_domain(entity, max_depth=settings.activities_depth)
        return None

    async def create(self, data: ActivityIn) -> Activity:
        entity = await self._create(data.model_dump())
        return to_domain(entity, max_depth=settings.activities_depth)

    async def update(self, act_id: UUID, data: ActivityUpdate) -> Activity:
        entity = await self._update_by_id(act_id, data.model_dump())
        return to_domain(entity, max_depth=settings.activities_depth)

    async def delete_by_id(self, act_id: UUID) -> Activity:
        entity = await self._get_by_id(act_id)
        if entity is None:
            raise NotFound.domain_entity(Activity, act_id)
        domain = to_domain(entity, max_depth=settings.activities_depth)
        await self._delete(act_id)
        return domain

    def _tree_loader(self):
        loader = selectinload(ActivityOrm.children)
        for _ in range(settings.activities_depth):
            loader = loader.selectinload(ActivityOrm.children)
        return loader

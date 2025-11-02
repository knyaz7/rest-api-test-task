from math import pi
from uuid import UUID

from sqlalchemy import Float, Integer, Select, and_, cast, func, literal, select
from sqlalchemy.orm import selectinload

from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.organizations.dto import (
    GeoBBox,
    GeoFilter,
    GeoRadius,
    OrganizationIn,
    OrganizationUpdate,
)
from rest_api_test.application.organizations.repo import OrganizationRepository
from rest_api_test.domain.organizations.model import Organization
from rest_api_test.infrastructure.sqlalchemy.activities.table import ActivityOrm
from rest_api_test.infrastructure.sqlalchemy.buildings.table import BuildingOrm
from rest_api_test.infrastructure.sqlalchemy.map_tables.org_activity import (
    OrganizationActivityMapOrm,
)
from rest_api_test.infrastructure.sqlalchemy.map_tables.org_pnumbers import (
    OrganizationPNumbersMapOrm,
)
from rest_api_test.infrastructure.sqlalchemy.organizations.mapper import to_domain
from rest_api_test.infrastructure.sqlalchemy.setup.base_repo import AlchemyRepo
from rest_api_test.utils.config.settings import get_settings

from .table import OrganizationOrm

settings = get_settings()


class AlchemyOrganizationRepo(OrganizationRepository, AlchemyRepo[OrganizationOrm]):
    model = OrganizationOrm

    async def get_all(
        self,
        pagination: Pagination | None = None,
        name: str | None = None,
        building_id: UUID | None = None,
        activity_id: UUID | None = None,
        geo: GeoFilter | None = None,
    ) -> list[Organization]:
        query = (
            select(OrganizationOrm)
            .distinct(OrganizationOrm.id)
            .options(self._activities_tree_loader())
        )

        if name:
            pattern = f"%{name}%"
            query = query.where(OrganizationOrm.name.ilike(pattern))

        if building_id:
            query = query.where(OrganizationOrm.building_id == building_id)

        if activity_id:
            activity_ids_stmt = self._activity_ids_with_descendants(activity_id)

            query = query.join(
                OrganizationActivityMapOrm,
                OrganizationActivityMapOrm.organization_id == OrganizationOrm.id,
            ).where(OrganizationActivityMapOrm.activity_id.in_(activity_ids_stmt))

        if geo:
            query = self._apply_geo_filter(query, geo)

        if pagination:
            query = query.limit(pagination.limit).offset(pagination.offset)

        res = await self._session.execute(query)
        rows = res.scalars().all()

        return [to_domain(o) for o in rows]

    async def get_by_id(self, org_id: UUID) -> Organization | None:
        query = (
            select(OrganizationOrm)
            .distinct(OrganizationOrm.id)
            .where(OrganizationOrm.id == org_id)
            .options(self._activities_tree_loader())
        )
        res = await self._session.scalar(query)
        if res:
            return to_domain(res)
        return None

    async def create(self, payload: OrganizationIn) -> Organization:
        org = await self._create(payload.model_dump())
        return to_domain(org)

    async def assign_phone_numbers(self, org_id: UUID, ids: list[UUID]) -> None:
        payload = [
            {"organization_id": org_id, "phone_number_id": phone_id} for phone_id in ids
        ]
        await self._add_relation(OrganizationPNumbersMapOrm, payload)

    async def unassign_phone_numbers(self, org_id: UUID, ids: list[UUID]) -> None:
        if not ids:
            return
        await self._drop_relation(
            OrganizationPNumbersMapOrm,
            OrganizationPNumbersMapOrm.organization_id == org_id,
            OrganizationPNumbersMapOrm.phone_number_id.in_(ids),
        )

    async def assign_activities(self, org_id: UUID, ids: list[UUID]) -> None:
        payload = [
            {"organization_id": org_id, "activity_id": activity_id}
            for activity_id in ids
        ]
        await self._add_relation(OrganizationActivityMapOrm, payload)

    async def unassign_activities(self, org_id: UUID, ids: list[UUID]) -> None:
        if not ids:
            return
        await self._drop_relation(
            OrganizationActivityMapOrm,
            OrganizationActivityMapOrm.organization_id == org_id,
            OrganizationActivityMapOrm.activity_id.in_(ids),
        )

    async def update_by_id(
        self, org_id: UUID, payload: OrganizationUpdate
    ) -> Organization:
        res = await self._update_by_id(org_id, payload.model_dump())
        return to_domain(res)

    async def delete_by_id(self, org_id: UUID) -> None:
        await self._delete(org_id)

    def _activities_tree_loader(self):
        """
        Builds a nested selectinload chain for
        OrganizationOrm.activities -> ActivityOrm.children
        to the depth settings.activities_depth.
        """
        loader = selectinload(OrganizationOrm.activities)
        for _ in range(settings.activities_depth):
            loader = loader.selectinload(ActivityOrm.children)
        return loader

    def _activity_ids_with_descendants(self, root_id: UUID) -> Select[tuple[UUID]]:
        base = (
            select(
                ActivityOrm.id.label("id"), literal(0, type_=Integer()).label("depth")
            )
            .where(ActivityOrm.id == root_id)
            .cte(name="activity_tree", recursive=True)
        )

        children = (
            select(ActivityOrm.id.label("id"), (base.c.depth + 1).label("depth"))
            .join(ActivityOrm, ActivityOrm.parent_id == base.c.id)
            .where(base.c.depth + 1 <= settings.activities_depth)
        )

        tree = base.union_all(children)

        return select(tree.c.id)

    def _apply_geo_filter(
        self, query: Select[tuple[OrganizationOrm]], geo: GeoFilter
    ) -> Select[tuple[OrganizationOrm]]:
        query = query.join(BuildingOrm, BuildingOrm.id == OrganizationOrm.building_id)

        if isinstance(geo, GeoRadius):
            lat = cast(BuildingOrm.latitude, Float())
            lon = cast(BuildingOrm.longitude, Float())

            lat0 = float(geo.lat)
            lon0 = float(geo.lon)
            radius_m = float(geo.radius_m)

            # перевод в радианы
            lat_rad = lat * (pi / 180.0)
            lon_rad = lon * (pi / 180.0)
            lat0_rad = literal(lat0 * (pi / 180.0))
            lon0_rad = literal(lon0 * (pi / 180.0))

            dlat = lat_rad - lat0_rad
            dlon = lon_rad - lon0_rad

            a = func.pow(func.sin(dlat / 2.0), 2) + func.cos(lat0_rad) * func.cos(
                lat_rad
            ) * func.pow(func.sin(dlon / 2.0), 2)
            c = 2.0 * func.atan2(func.sqrt(a), func.sqrt(1.0 - a))
            distance_m = settings.earth_radius_m * c

            query = query.where(distance_m <= radius_m)

        elif isinstance(geo, GeoBBox):
            query = query.where(
                and_(
                    BuildingOrm.latitude >= geo.lat_min,
                    BuildingOrm.latitude <= geo.lat_max,
                    BuildingOrm.longitude >= geo.lon_min,
                    BuildingOrm.longitude <= geo.lon_max,
                )
            )
        else:
            pass

        return query

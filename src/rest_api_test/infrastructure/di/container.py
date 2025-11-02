from dependency_injector import containers, providers
from redis.asyncio import Redis  # type: ignore[reportMissingTypeStubs]

from rest_api_test.application.activities.service import ActivityService
from rest_api_test.application.buildings.service import BuildingService
from rest_api_test.application.data_filler.filler import DataFiller
from rest_api_test.application.organizations.service import OrganizationService
from rest_api_test.application.phone_numbers.service import PhoneNumberService
from rest_api_test.infrastructure.redis.cache import RedisCache
from rest_api_test.infrastructure.sqlalchemy.activities.repo import AlchemyActivityRepo
from rest_api_test.infrastructure.sqlalchemy.buildings.repo import AlchemyBuildingRepo
from rest_api_test.infrastructure.sqlalchemy.organizations.repo import (
    AlchemyOrganizationRepo,
)
from rest_api_test.infrastructure.sqlalchemy.phone_numbers.repo import (
    AlchemyPhoneNumberRepo,
)
from rest_api_test.infrastructure.sqlalchemy.setup.engine import async_session_factory
from rest_api_test.infrastructure.sqlalchemy.uow import AlchemyUnitOfWork
from rest_api_test.utils.config.settings import get_settings

settings = get_settings()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["rest_api_test.infrastructure.fastapi.endpoints.v1"]
    )  # fastapi integration

    redis = providers.Singleton(
        Redis.from_url,  # type: ignore[reportUnknownMemberType]
        settings.redis_dsn,
    )

    key_value_cache = providers.Singleton(RedisCache, redis_client=redis)

    al_session = providers.ContextLocalSingleton(async_session_factory)

    alchemy_uow = providers.Factory(AlchemyUnitOfWork, session=al_session)

    orgs_repo = providers.Factory(AlchemyOrganizationRepo, session=al_session)
    acts_repo = providers.Factory(AlchemyActivityRepo, session=al_session)
    pn_repo = providers.Factory(AlchemyPhoneNumberRepo, session=al_session)
    blds_repo = providers.Factory(AlchemyBuildingRepo, session=al_session)

    orgs_service = providers.Factory(
        OrganizationService,
        uow=alchemy_uow,
        orgs_repo=orgs_repo,
        build_repo=blds_repo,
        activity_repo=acts_repo,
        phone_repo=pn_repo,
    )
    activities_service = providers.Factory(
        ActivityService, uow=alchemy_uow, repo=acts_repo
    )
    buildings_service = providers.Factory(
        BuildingService, uow=alchemy_uow, repo=blds_repo
    )
    phone_numbers_service = providers.Factory(
        PhoneNumberService, uow=alchemy_uow, repo=pn_repo
    )
    data_filler = providers.Factory(
        DataFiller,
        org_repo=orgs_repo,
        activity_repo=acts_repo,
        pn_repo=pn_repo,
        building_repo=blds_repo,
        uow=alchemy_uow,
    )

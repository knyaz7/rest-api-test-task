from dependency_injector import containers, providers
from redis.asyncio import Redis  # type: ignore[reportMissingTypeStubs]

from rest_api_test.application.organizations.service import OrganizationService
from rest_api_test.infrastructure.redis.cache import RedisCache
from rest_api_test.infrastructure.sqlalchemy.organizations.repo import (
    AlchemyOrganizationRepo,
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

    orgs_repo = providers.Factory(
        AlchemyOrganizationRepo, session=al_session
    )
    orgs_service = providers.Factory(
        OrganizationService, uow=alchemy_uow, users_repo=orgs_repo
    )

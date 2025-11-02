from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from rest_api_test.infrastructure.di.container import Container
from rest_api_test.infrastructure.fastapi.middlewares.api_key import (
    enable_api_key_in_swagger,
    register_api_key_middleware,
)
from rest_api_test.utils.config.settings import get_settings

from .endpoints import api_v1_router
from .error_handler import register_error_handlers

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()

    redis = container.redis()

    app.container = container  # type: ignore[reportAttributeAccessIssue]
    redis = container.redis()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    yield
    await redis.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan, docs_url="/api/docs")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_api_key_middleware(
        app, header_name=settings.api_token_header_name, api_key=settings.api_token
    )
    enable_api_key_in_swagger(app, settings.api_token_header_name)
    app.include_router(api_v1_router)
    register_error_handlers(app)
    return app

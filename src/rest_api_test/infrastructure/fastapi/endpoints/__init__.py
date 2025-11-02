from fastapi import APIRouter

from .v1.activities import activities_router
from .v1.buildings import buildings_router
from .v1.db_filler import fillers_router
from .v1.organizations import organizations_router
from .v1.phone_numbers import phone_numbers_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(organizations_router)
api_v1_router.include_router(buildings_router)
api_v1_router.include_router(activities_router)
api_v1_router.include_router(phone_numbers_router)
api_v1_router.include_router(fillers_router)

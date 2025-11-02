from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from rest_api_test.application.data_filler.filler import DataFiller
from rest_api_test.infrastructure.di.container import Container

fillers_router = APIRouter(prefix="/filler", tags=["Database filler"])


@fillers_router.post("/fill", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def fill_database(
    data_filler: Annotated[DataFiller, Depends(Provide[Container.data_filler])],
):
    await data_filler.fill_database()

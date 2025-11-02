from fastapi import Query

from rest_api_test.application.interfaces.common.pagination import Pagination


def get_pagination(
    limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)
) -> Pagination:
    return Pagination(limit=limit, offset=offset)

from rest_api_test.domain.activities.model import Activity
from rest_api_test.utils.config.settings import get_settings

from .table import ActivityOrm

settings = get_settings()


def to_domain(entity: ActivityOrm, *, max_depth: int | None = None) -> Activity:
    depth_limit = max_depth if max_depth is not None else settings.activities_depth
    return _map_activity(entity, current_depth=0, depth_limit=depth_limit)


def _map_activity(
    entity: ActivityOrm, *, current_depth: int, depth_limit: int
) -> Activity:
    children: list[Activity] | None = None

    if current_depth < depth_limit:
        mapped_children = [
            _map_activity(
                child, current_depth=current_depth + 1, depth_limit=depth_limit
            )
            for child in entity.children
        ]
        if mapped_children:
            children = mapped_children

    return Activity(
        id=entity.id, name=entity.name, parent_id=entity.parent_id, children=children
    )

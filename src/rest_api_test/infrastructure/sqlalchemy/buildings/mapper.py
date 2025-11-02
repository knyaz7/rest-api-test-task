from rest_api_test.domain.buildings.model import Building

from .table import BuildingOrm


def to_domain(entity: BuildingOrm) -> Building:
    return Building(
        id=entity.id,
        address=entity.address,
        latitude=entity.latitude,
        longitude=entity.longitude,
    )

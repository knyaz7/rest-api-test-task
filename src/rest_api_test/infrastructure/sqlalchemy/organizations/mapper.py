from rest_api_test.domain.activities.model import Activity
from rest_api_test.domain.organizations.model import Organization
from rest_api_test.domain.phone_numbers.table import PhoneNumber

from .table import OrganizationOrm


def to_domain(orm: OrganizationOrm) -> Organization:
    return Organization(
        id=orm.id,
        name=orm.name,
        building_id=orm.building_id,
        activities=[
            Activity(id=a.id, name=a.name, parent_id=a.parent_id)
            for a in orm.activities
        ],
        phone_numbers=[
            PhoneNumber(id=p.id, phone_number=p.phone_number) for p in orm.phone_numbers
        ],
    )

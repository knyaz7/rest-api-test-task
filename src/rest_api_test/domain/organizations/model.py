from dataclasses import dataclass
from uuid import UUID

from rest_api_test.domain.activities.model import Activity
from rest_api_test.domain.phone_numbers.table import PhoneNumber


@dataclass(frozen=True)
class Organization:
    id: UUID
    name: str
    phone_numbers: list[PhoneNumber]
    activities: list[Activity]
    building_id: UUID

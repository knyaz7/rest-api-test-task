from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class Building:
    id: UUID
    address: str
    latitude: Decimal
    longitude: Decimal

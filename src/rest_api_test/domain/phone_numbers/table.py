from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class PhoneNumber:
    id: UUID
    phone_number: str

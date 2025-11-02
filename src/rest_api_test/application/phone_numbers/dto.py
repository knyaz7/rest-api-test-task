from uuid import UUID

from pydantic import BaseModel


class PhoneNumberIn(BaseModel):
    phone_number: str


class PhoneNumberUpdate(PhoneNumberIn):
    pass


class PhoneNumberOut(PhoneNumberIn):
    id: UUID

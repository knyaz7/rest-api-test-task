from abc import ABC, abstractmethod
from uuid import UUID

from rest_api_test.application.interfaces.common.pagination import Pagination
from rest_api_test.application.phone_numbers.dto import PhoneNumberIn, PhoneNumberUpdate
from rest_api_test.domain.phone_numbers.table import PhoneNumber


class PhoneNumberRepository(ABC):
    @abstractmethod
    async def get_all(self, pagination: Pagination) -> list[PhoneNumber]: ...

    @abstractmethod
    async def get_by_id(self, pn_id: UUID) -> PhoneNumber | None: ...

    @abstractmethod
    async def create(self, data: PhoneNumberIn) -> PhoneNumber: ...

    @abstractmethod
    async def update(self, pn_id: UUID, data: PhoneNumberUpdate) -> PhoneNumber: ...

    @abstractmethod
    async def delete_by_id(self, pn_id: UUID) -> PhoneNumber: ...

from rest_api_test.domain.phone_numbers.table import PhoneNumber

from .table import PhoneNumberOrm


def to_domain(entity: PhoneNumberOrm) -> PhoneNumber:
    return PhoneNumber(id=entity.id, phone_number=entity.phone_number)

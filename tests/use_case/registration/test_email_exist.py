# -*- coding: utf8 -*-
from typing import List, Union

from nest.app.entity.location import Location
from nest.app.entity.user import IUserRepository, User
from nest.app.use_case.registration import (
    EmailOccupyError,
    IParams,
    RegistrationUseCase,
)
from tests.use_case import EmptyLocationRepository
from tests.use_case.registration.mock_mail_service import MockMailService


class MockLocationRepository(EmptyLocationRepository):
    def add(self, *, location: Location):
        pass

    def clear(self):
        pass

    def find(self, *, page: int, per_page: int, user_id: int):
        pass

    def get(self, *, id_: int) -> Union[None, Location]:
        pass

    def get_default(self, *, user_id: int) -> Union[None, Location]:
        pass


class MockParams(IParams):
    def get_email(self):
        return 'foo@bar.com'

    def get_nickname(self):
        return '溜兔子'

    def get_password(self):
        return '123456'


class MockUserRepository(IUserRepository):
    def add(self, user: User):
        pass

    def clear(self):
        pass

    def find(self, *, page: int, per_page: int) -> List[User]:
        pass

    def get_by_email(self, email):
        assert email == 'foo@bar.com'
        return {
            'email': email,
        }


def test_email_exist():
    use_case = RegistrationUseCase(
        location_repository=MockLocationRepository(),
        mail_service=MockMailService(),
        params=MockParams(),
        user_repository=MockUserRepository(),
    )
    is_error_occur = False
    try:
        use_case.run()
    except EmailOccupyError:
        is_error_occur = True
    assert is_error_occur

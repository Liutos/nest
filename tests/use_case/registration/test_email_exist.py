# -*- coding: utf8 -*-
from typing import Union

from nest.app.entity.location import ILocationRepository, Location
from nest.app.entity.user import IUserRepository, User
from nest.app.use_case.registration import EmailOccupyError, IParams, \
    RegistrationUseCase


class MockLocationRepository(ILocationRepository):
    def add(self, *, location: Location):
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

    def get_by_email(self, email):
        assert email == 'foo@bar.com'
        return {
            'email': email,
        }


def test_email_exist():
    use_case = RegistrationUseCase(
        location_repository=MockLocationRepository(),
        params=MockParams(),
        user_repository=MockUserRepository(),
    )
    is_error_occur = False
    try:
        use_case.run()
    except EmailOccupyError:
        is_error_occur = True
    assert is_error_occur

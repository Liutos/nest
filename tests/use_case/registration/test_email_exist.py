# -*- coding: utf8 -*-
import pytest

from nest.app.entity.user import IUserRepository
from nest.app.use_case.registration import EmailOccupyError, IParams, \
    RegistrationUseCase


class MockParams(IParams):
    def get_email(self):
        return 'foo@bar.com'

    def get_nickname(self):
        return '溜兔子'

    def get_password(self):
        return '123456'


class MockUserRepository(IUserRepository):
    def add(self):
        pass

    def get_by_email(self, email):
        assert email == 'foo@bar.com'
        return {
            'email': email,
        }


def test_email_exist():
    use_case = RegistrationUseCase(
        params=MockParams(),
        user_repository=MockUserRepository(),
    )
    is_error_occur = False
    try:
        use_case.run()
    except EmailOccupyError:
        is_error_occur = True
    assert is_error_occur

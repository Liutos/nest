# -*- coding: utf8 -*-
import pytest

from nest.app.entity.user import IUserRepository, User
from nest.app.use_case.registration import IParams, \
    RegistrationUseCase


class MockRegistrationIO(IParams):
    def get_email(self) -> str:
        return 'foo@bar.com'

    def get_nickname(self) -> str:
        return '溜兔子'

    def get_password(self) -> str:
        return '123456'


class MockUserRepository(IUserRepository):
    def __init__(self):
        self.user = None

    def add(self, user: User):
        email = user.email
        assert email == 'foo@bar.com'
        self.user = user

    def get_by_email(self, email: str) -> User:
        assert email == 'foo@bar.com'
        return self.user


def test_add_user():
    use_case = RegistrationUseCase(
        params=MockRegistrationIO(),
        user_repository=MockUserRepository(),
    )
    user = use_case.run()
    assert user
    assert isinstance(user, User)

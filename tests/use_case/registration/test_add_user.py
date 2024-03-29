# -*- coding: utf8 -*-
from typing import List, Union

from nest.app.entity.location import Location
from nest.app.entity.user import IUserRepository, User
from nest.app.use_case.registration import (
    IParams,
    RegistrationUseCase,
)
from tests.use_case import EmptyLocationRepository
from tests.use_case.registration.mock_mail_service import MockMailService


class MockRegistrationIO(IParams):
    def get_email(self) -> str:
        return 'foo@bar.com'

    def get_nickname(self) -> str:
        return '溜兔子'

    def get_password(self) -> str:
        return '123456'


class MockLocationRepository(EmptyLocationRepository):
    def __init__(self):
        self.location = None

    def add(self, *, location: Location):
        location.id = 634
        self.location = location

    def clear(self):
        pass

    def find(self, *, page: int, per_page: int, user_id: int):
        pass

    def get(self, *, id_: int) -> Union[None, Location]:
        pass

    def get_default(self, *, user_id: int) -> Union[None, Location]:
        pass


class MockUserRepository(IUserRepository):
    def __init__(self):
        self.user = None

    def add(self, user: User):
        email = user.email
        assert email == 'foo@bar.com'
        self.user = user

    def clear(self):
        pass

    def find(self, *, page: int, per_page: int) -> List[User]:
        pass

    def get_by_email(self, email: str) -> User:
        assert email == 'foo@bar.com'
        return self.user


def test_add_user():
    location_repository = MockLocationRepository()
    use_case = RegistrationUseCase(
        location_repository=location_repository,
        mail_service=MockMailService(),
        params=MockRegistrationIO(),
        user_repository=MockUserRepository(),
    )
    user = use_case.run()
    assert user
    assert isinstance(user, User)
    assert location_repository.location.id == 634

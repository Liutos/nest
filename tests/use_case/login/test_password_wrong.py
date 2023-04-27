# -*- coding: utf8 -*-
from typing import List

from nest.app.entity.certificate import Certificate, ICertificateRepository
from nest.app.entity.user import IUserRepository, User, UserStatus
from nest.app.use_case.login import IParams, \
    LoginUseCase, PasswordError
from nest.service.authenticate_service import AuthenticateService


class MockLoginIO(IParams):
    def get_email(self):
        return 'mat.liutos@gmail.com'

    def get_password(self):
        return '1234567'


class MockSessionRepository(ICertificateRepository):
    def add(self, session):
        pass

    def get_by_certificate_id(self, certificate_id: int) -> Certificate:
        pass


class MockUserRepository(IUserRepository):
    def add(self, user: User):
        pass

    def clear(self):
        pass

    def find(self, *, page: int, per_page: int) -> List[User]:
        pass

    def get_by_email(self, email):
        user = User.new(
            'mat.liutos@gmail.com',
            'Liutos',
            '12345678',
        )
        user.status = UserStatus.ACTIVATED
        return user


def test_succeed():
    use_case = LoginUseCase(
        authenticate_service=AuthenticateService(MockUserRepository()),
        params=MockLoginIO(),
        certificate_repository=MockSessionRepository(),
    )
    is_error_occur = False
    try:
        use_case.run()
    except PasswordError:
        is_error_occur = True
    assert is_error_occur

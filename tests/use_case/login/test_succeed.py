# -*- coding: utf8 -*-
from nest.app.entity.certificate import Certificate, ICertificateRepository
from nest.app.entity.user import IUserRepository, User
from nest.app.use_case.login import IParams, \
    LoginUseCase


class MockLoginIO(IParams):
    def get_email(self):
        return 'mat.liutos@gmail.com'

    def get_password(self):
        return '1234567'


class MockCertificateRepository(ICertificateRepository):
    def add(self, certificate):
        certificate.id = 1

    def get_by_certificate_id(self, certificate_id: int) -> Certificate:
        pass


class MockUserRepository(IUserRepository):
    def add():
        pass

    def get_by_email(self, email):
        return User.new(
            'mat.liutos@gmail.com',
            'Liutos',
            '1234567',
        )


def test_succeed():
    use_case = LoginUseCase(
        params=MockLoginIO(),
        certificate_repository=MockCertificateRepository(),
        user_repository=MockUserRepository(),
    )
    session = use_case.run()
    assert session
    assert session.id

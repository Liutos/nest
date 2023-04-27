# -*- coding: utf8 -*-
from typing import Union, Optional, List

from nest.app.entity.certificate import Certificate, ICertificateRepository
from nest.app.entity.user import IUserRepository, User
from nest.app.use_case.authenticate import AuthenticateUseCase, IParams
from nest.service.authenticate_service import AuthenticateService

_user_id = 233


class MockCertificateRepository(ICertificateRepository):
    def add(self, certificate: Certificate):
        pass

    def get_by_certificate_id(self, certificate_id: str) -> Certificate:
        return Certificate.new(_user_id)


class MockParams(IParams):
    def get_certificate_id(self) -> Union[None, str]:
        return 'abc'

    def get_email(self) -> Optional[str]:
        pass

    def get_password(self) -> Optional[str]:
        pass

    def get_user_id(self) -> Union[None, int]:
        return _user_id


class MockUserRepository(IUserRepository):
    def add(self, user: User):
        pass

    def clear(self):
        pass

    def find(self, *, page: int, per_page: int) -> List[User]:
        pass

    def get_by_email(self, email: str) -> Optional[User]:
        pass


def test_authentication():
    """测试认证的正常逻辑。"""
    use_case = AuthenticateUseCase(
        authenticate_service=AuthenticateService(MockUserRepository()),
        certificate_repository=MockCertificateRepository(),
        params=MockParams(),
    )
    use_case.run()

# -*- coding: utf8 -*-
from typing import Union

from nest.app.entity.certificate import Certificate, ICertificateRepository
from nest.app.use_case.authenticate import AuthenticateUseCase, IParams


_user_id = 233


class MockCertificateRepository(ICertificateRepository):
    def add(self, certificate: Certificate):
        pass

    def get_by_certificate_id(self, certificate_id: str) -> Certificate:
        return Certificate.new(_user_id)


class MockParams(IParams):
    def get_certificate_id(self) -> Union[None, str]:
        return 'abc'

    def get_user_id(self) -> Union[None, int]:
        return _user_id


def test_authentication():
    """测试认证的正常逻辑。"""
    use_case = AuthenticateUseCase(
        certificate_repository=MockCertificateRepository(),
        params=MockParams(),
    )
    use_case.run()

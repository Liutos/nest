# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Union

from nest.app.entity.certificate import ICertificateRepository


class IParams(ABC):
    @abstractmethod
    def get_certificate_id(self) -> Union[None, str]:
        pass

    @abstractmethod
    def get_user_id(self) -> Union[None, int]:
        pass


class AuthenticateFailError(Exception):
    pass


class CertificateIdMissingError(Exception):
    pass


class CertificateNotFoundError(Exception):
    pass


class UserIdMissingError(Exception):
    pass


class AuthenticateUseCase:
    def __init__(self, *, certificate_repository, params):
        assert isinstance(certificate_repository, ICertificateRepository)
        assert isinstance(params, IParams)
        self.certificate_repository = certificate_repository
        self.params = params

    def run(self) -> int:
        """
        Raises:
            CertificateIdMissingError: 如果缺少登录凭证的 ID。
            CertificateNotFoundError: 如果 ID 找不到登录凭证。
            UserIdMissingError: 如果缺少用户 ID。
            AuthenticateFailError: 如果登录凭证与用户不匹配。

        Returns:
            int: 认证通过的用户的 ID。
        """
        params = self.params
        certificate_id = params.get_certificate_id()
        if not certificate_id:
            raise CertificateIdMissingError()

        certificate_repository = self.certificate_repository
        certificate = certificate_repository.get_by_certificate_id(certificate_id)
        if not certificate:
            raise CertificateNotFoundError()

        user_id = params.get_user_id()
        if not user_id:
            raise UserIdMissingError()

        if user_id != certificate.user_id:
            raise AuthenticateFailError()

        return user_id

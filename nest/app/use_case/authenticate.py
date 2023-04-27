# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Optional, Union

from nest.app.entity.certificate import ICertificateRepository
from nest.app.use_case.login import IAuthenticateService


class IParams(ABC):
    @abstractmethod
    def get_certificate_id(self) -> Union[None, str]:
        pass

    @abstractmethod
    def get_email(self) -> Optional[str]:
        """获取用于认证身份的邮箱。"""
        pass

    @abstractmethod
    def get_password(self) -> Optional[str]:
        """获取与邮箱配套的密码。"""
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
    def __init__(self, *, authenticate_service: IAuthenticateService, certificate_repository, params):
        assert isinstance(certificate_repository, ICertificateRepository)
        assert isinstance(params, IParams)
        self._authenticate_service = authenticate_service
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
        email = params.get_email()
        password = params.get_password()
        if email and password:
            return self._authenticate_by_email_password(email, password)

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

    def _authenticate_by_email_password(self, email: str, password: str) -> int:
        user = self._authenticate_service.check_is_email_password_match(email, password)
        return user.id

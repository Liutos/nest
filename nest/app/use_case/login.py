# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from ..entity.certificate import Certificate, ICertificateRepository
from ..entity.user import User


class PasswordError(Exception):
    pass


class UserNotActive(Exception):
    """表示所要登录的用户尚未激活的异常。"""
    pass


class IAuthenticateService(ABC):
    """实现该接口的类将会提供认证身份的服务。"""
    @abstractmethod
    def check_is_email_password_match(self, email: str, password: str) -> User:
        """
        如果邮箱与密码匹配，则返回该邮箱对应的用户，否则抛出各个场景对应的异常。

        :raises PasswordError: 用户不存在或密码不正确时抛出该异常。
        :raises UserNotActive: 用户未激活时抛出该异常。
        """
        pass


class IParams(ABC):
    @abstractmethod
    def get_email(self) -> str:
        pass

    @abstractmethod
    def get_password(self) -> str:
        pass


class LoginUseCase:
    def __init__(self, *, authenticate_service: IAuthenticateService, params,
                 certificate_repository):
        assert isinstance(params, IParams)
        assert isinstance(certificate_repository, ICertificateRepository)
        self._authenticate_service = authenticate_service
        self.params = params
        self.certificate_repository = certificate_repository

    def run(self):
        login_io = self.params
        email = login_io.get_email()
        password = login_io.get_password()
        user = self._authenticate_service.check_is_email_password_match(email, password)

        certificate = Certificate.new(user.id)
        self.certificate_repository.add(certificate)
        return certificate

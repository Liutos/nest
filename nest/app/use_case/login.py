# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from ..entity.certificate import Certificate, ICertificateRepository
from ..entity.user import IUserRepository


class PasswordError(Exception):
    pass


class IParams(ABC):
    @abstractmethod
    def get_email(self) -> str:
        pass

    @abstractmethod
    def get_password(self) -> str:
        pass


class LoginUseCase():
    def __init__(self, *, params,
                 certificate_repository, user_repository):
        assert isinstance(params, IParams)
        assert isinstance(certificate_repository, ICertificateRepository)
        assert isinstance(user_repository, IUserRepository)
        self.params = params
        self.certificate_repository = certificate_repository
        self.user_repository = user_repository

    def run(self):
        login_io = self.params
        user_repository = self.user_repository
        email = login_io.get_email()
        user = user_repository.get_by_email(email)
        if not user:
            raise PasswordError()

        password = login_io.get_password()
        is_match = user.test_password(password)
        if not is_match:
            raise PasswordError()

        certificate = Certificate.new(user.id)
        self.certificate_repository.add(certificate)
        return certificate

# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from flask import request

from nest.app.entity.certificate import ICertificateRepository
from nest.app.use_case.authentication_plugin import IAuthenticationPlugin, InvalidCertificateError


class IParams(ABC):
    @abstractmethod
    def get_certificate_id(self) -> str:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class AuthenticationParamsMixin(IParams):
    def get_certificate_id(self) -> int:
        return request.cookies.get('certificate_id')

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


class AuthenticationPlugin(IAuthenticationPlugin):
    def __init__(self, *, certificate_repository, params):
        assert isinstance(certificate_repository, ICertificateRepository)
        assert isinstance(params, IParams)
        self.certificate_repository = certificate_repository
        self.params = params

    def authenticate(self):
        certificate_repository = self.certificate_repository
        params = self.params
        certificate_id = params.get_certificate_id()
        user_id = params.get_user_id()
        certificate = certificate_repository.get_by_certificate_id(certificate_id)
        if certificate is None:
            raise InvalidCertificateError()
        if user_id != certificate.user_id:
            raise InvalidCertificateError()

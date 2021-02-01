# -*- coding: utf8 -*-
from nest.app.entity.certificate import ICertificateRepository
from nest.app.use_case.authentication_plugin import IAuthenticationPlugin, InvalidCertificateError


class AuthenticationPlugin(IAuthenticationPlugin):
    def __init__(self, *, certificate_repository, params):
        assert isinstance(certificate_repository, ICertificateRepository)
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

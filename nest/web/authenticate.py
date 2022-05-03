# -*- coding: utf8 -*-
import functools

from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.web import certificate
from nest.web.cookies_params import CookiesParams


def authenticate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        certificate_repository = certificate.get_repository()
        authenticate_use_case = AuthenticateUseCase(
            certificate_repository=certificate_repository,
            params=CookiesParams(),
        )
        authenticate_use_case.run()
        return func(*args, **kwargs)

    return wrapper

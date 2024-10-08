# -*- coding: utf8 -*-
import functools

from nest.infra.db_connection import DBUtilsConnectionPool
from nest.infra.repository import MysqlUnitOfWork

from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.service.authenticate_service import AuthenticateService
from nest.web import certificate, config
from nest.web.cookies_params import CookiesParams


def authenticate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        certificate_repository = certificate.get_repository()
        mysql_connection = DBUtilsConnectionPool(config.get_config())
        repository_factory = MysqlUnitOfWork(mysql_connection)
        user_repository = repository_factory.user()
        authenticate_use_case = AuthenticateUseCase(
            authenticate_service=AuthenticateService(user_repository),
            certificate_repository=certificate_repository,
            params=CookiesParams(),
        )
        user_id = authenticate_use_case.run()
        return func(*args, **{**kwargs, 'user_id': user_id})

    return wrapper

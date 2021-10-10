# -*- coding: utf8 -*-
from flask import request

from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.delete_location import (
    DeleteLocationUseCase,
    IParams,
    LocationInUseError,
)
from nest.infra.repository import RepositoryFactory
from nest.web.cookies_params import CookiesParams
from nest.web.handle_response import wrap_response


class HTTPParams(IParams):
    def __init__(self, *, location_id):
        self.location_id = location_id

    def get_location_id(self) -> int:
        return self.location_id

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


@wrap_response
def delete_location(certificate_repository, id_, repository_factory: RepositoryFactory):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams(
        location_id=id_,
    )
    use_case = DeleteLocationUseCase(
        location_repository=repository_factory.location(),
        params=params,
        plan_repository=repository_factory.plan(),
    )
    try:
        use_case.run()
        return {
            'error': None,
            'result': None,
            'status': 'success',
        }, 200
    except LocationInUseError as e:
        message = '地点{}被计划{}所使用，无法删除'.format(id_, e.plan_id)
        return {
            'error': {
                'code': 422,
                'message': message,
            },
            'result': None,
            'status': 'failure',
        }, 422

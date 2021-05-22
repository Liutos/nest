# -*- coding: utf8 -*-
from flask import request

from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.get_location import (
    AccessDeniedError,
    GetLocationUseCase,
    IParams,
)
from nest.web.cookies_params import CookiesParams
from nest.web.handle_response import wrap_response
from nest.web.presenter.location import LocationPresenter


class HTTPParams(IParams):
    def __init__(self, *, location_id: str):
        self.location_id = int(location_id)

    def get_id(self) -> int:
        return self.location_id

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


@wrap_response
def get_location(certificate_repository, id_, repository_factory):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams(location_id=id_)
    use_case = GetLocationUseCase(
        location_repository=repository_factory.location(),
        params=params,
    )
    try:
        location = use_case.run()
    except AccessDeniedError:
        return {
            'error': {
                'code': 403,
                'message': '无权查看该地点'
            },
            'result': None,
            'status': 'failure',
        }

    presenter = LocationPresenter(
        location=location,
    )
    return {
        'error': None,
        'result': presenter.format(),
        'status': 'success',
    }, 200

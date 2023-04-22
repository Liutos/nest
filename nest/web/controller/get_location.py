# -*- coding: utf8 -*-
from flask import request

from nest.app.use_case.get_location import (
    GetLocationUseCase,
    IParams,
)
from nest.app.entity.location import AccessDeniedError
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.presenter.location import LocationPresenter


class HTTPParams(IParams):
    def __init__(self, *, location_id: str, user_id: int):
        self._user_id = user_id
        self.location_id = int(location_id)

    def get_id(self) -> int:
        return self.location_id

    def get_user_id(self) -> int:
        return self._user_id


@wrap_response
@authenticate
def get_location(id_, repository_factory, user_id: int, **kwargs):
    params = HTTPParams(location_id=id_, user_id=user_id)
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

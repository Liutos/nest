# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from nest.app.use_case.create_location import (
    CreateLocationUseCase,
    IParams,
)
from nest.infra.repository import RepositoryFactory
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.location import LocationPresenter


class HTTPParams(IParams):
    def __init__(self, user_id: int):
        args = {
            'name': fields.Str(required=True),
        }
        parsed_args = parser.parse(args, request)
        self._user_id = user_id
        self.name = parsed_args['name']

    def get_name(self) -> str:
        return self.name

    def get_user_id(self) -> int:
        return self._user_id


@wrap_response  # wrap_response 必须位于最外层，否则无法处理认证失败的异常。
@authenticate
def create_location(repository_factory: RepositoryFactory,
                    user_id: int,
                    **kwargs):
    use_case = CreateLocationUseCase(
        location_repository=repository_factory.location(),
        params=HTTPParams(user_id),
    )
    location = use_case.run()
    presenter = LocationPresenter(location=location)
    return {
        'error': None,
        'result': presenter.format(),
        'status': 'success',
    }, 201

# -*- coding: utf8 -*-
from typing import Union

from flask import request
from webargs import fields

from nest.app.use_case.pop_plan import IParams, PopPlanUseCase
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.plan import PlanPresenter


class HTTPParams(IParams):
    def __init__(self, user_id: int):
        args = {
            'location_id': fields.Int(allow_none=True),
            'size': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request)
        self._user_id = user_id
        self.location_id = parsed_args.get('location_id')
        self.size = parsed_args['size']

    def get_location_id(self) -> Union[None, int]:
        return self.location_id

    def get_size(self) -> int:
        return self.size

    def get_user_id(self) -> int:
        return self._user_id


@wrap_response
@authenticate
def pop_plan(repository_factory, *, user_id: int, **kwargs):
    params = HTTPParams(user_id)
    use_case = PopPlanUseCase(
        location_repository=repository_factory.location(),
        params=params,
        plan_repository=repository_factory.plan(),
    )
    plans = use_case.run()
    return {
        'error': None,
        'result': [PlanPresenter(plan=plan).format() for plan in plans],
        'status': 'success',
    }, 200

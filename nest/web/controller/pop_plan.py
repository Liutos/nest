# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.pop_plan import IParams, PopPlanUseCase
from nest.web.cookies_params import CookiesParams
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.plan import PlanPresenter


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'size': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request)
        self.size = parsed_args['size']

    def get_size(self) -> int:
        return self.size

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


@wrap_response
def pop_plan(certificate_repository, repository_factory):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams()
    use_case = PopPlanUseCase(
        params=params,
        plan_repository=repository_factory.plan(),
    )
    plans = use_case.run()
    return {
        'error': None,
        'result': [PlanPresenter(plan=plan).format() for plan in plans],
        'status': 'success',
    }, 200

# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from ...app.use_case.pop_plan import IParams, PopPlanUseCase
from nest.web.authentication_plugin import (
    AuthenticationPlugin,
    AuthenticationParamsMixin,
)
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.plan import PlanPresenter


class HTTPParams(AuthenticationParamsMixin, IParams):
    def __init__(self):
        args = {
            'size': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request)
        self.size = parsed_args['size']

    def get_size(self) -> int:
        return self.size


@wrap_response
def pop_plan(certificate_repository, repository_factory):
    params = HTTPParams()
    authentication_plugin = AuthenticationPlugin(
        certificate_repository=certificate_repository,
        params=params
    )
    use_case = PopPlanUseCase(
        authentication_plugin=authentication_plugin,
        params=params,
        plan_repository=repository_factory.plan(),
    )
    plans = use_case.run()
    return {
        'error': None,
        'result': [PlanPresenter(plan=plan).format() for plan in plans],
        'status': 'success',
    }, 200

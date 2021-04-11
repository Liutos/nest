# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from ...app.use_case.pop_plan import IParams, PopPlanUseCase
from nest.web.authentication_plugin import AuthenticationPlugin, IParams as AuthenticationParams
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.plan import PlanPresenter


class HTTPParams(AuthenticationParams, IParams):
    def __init__(self):
        args = {
            'size': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request)
        self.size = parsed_args['size']
        args = {
            'certificate_id': fields.Str(required=True),
            'user_id': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request, location='cookies')
        self.certificate_id = parsed_args['certificate_id']
        self.user_id = parsed_args['user_id']

    def get_certificate_id(self):
        return self.certificate_id

    def get_size(self) -> int:
        return self.size

    def get_user_id(self):
        return self.user_id


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
        'plans': [PlanPresenter(plan=plan).format() for plan in plans],
    }, 200

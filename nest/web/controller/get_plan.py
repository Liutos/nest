# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from nest.app.use_case.get_plan import GetPlanUseCase, IParams
from nest.web.authentication_plugin import AuthenticationPlugin, IParams as AuthenticationParams
from nest.web.parser import parser
from nest.web.handle_response import wrap_response


class HTTPParams(AuthenticationParams, IParams):
    def __init__(self, *, plan_id):
        self.plan_id = plan_id
        args = {
            'certificate_id': fields.Str(required=True),
            'user_id': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request, location='cookies')
        self.certificate_id = parsed_args['certificate_id']
        self.user_id = parsed_args['user_id']

    def get_certificate_id(self) -> str:
        return self.certificate_id

    def get_plan_id(self) -> int:
        return self.plan_id

    def get_user_id(self) -> int:
        return self.user_id


@wrap_response
def get_plan(certificate_repository, id_, repository_factory):
    params = HTTPParams(plan_id=id_)
    use_case = GetPlanUseCase(
        authentication_plugin=AuthenticationPlugin(
            certificate_repository=certificate_repository,
            params=params,
        ),
        params=params,
        plan_repository=repository_factory.plan(),
    )
    plan = use_case.run()
    if plan is None:
        return {
            'error': None,
            'result': None,
            'status': 'success',
        }, 200
    return {
        'error': None,
        'result': {
            'id': plan.id,
            'task_id': plan.task_id,
            'trigger_time': plan.trigger_time,
        },
        'status': 'success',
    }, 200

# -*- coding: utf8 -*-
from datetime import datetime

from flask import request
from webargs import fields

from ...app.use_case.create_plan import CreatePlanUseCase, IParams
from ..repository import RepositoryFactory
from nest.web.authentication_plugin import AuthenticationPlugin, IParams as AuthenticationParams
from nest.web.certificate_repository import certificate_repository
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(AuthenticationParams, IParams):
    def __init__(self):
        args = {
            'task_id': fields.Int(required=True),
            'trigger_time': fields.DateTime('%Y-%m-%d %H:%M:%S', required=True),
        }
        parsed_args = parser.parse(args, request)
        self.task_id = parsed_args['task_id']
        self.trigger_time = parsed_args['trigger_time']
        args = {
            'certificate_id': fields.Int(required=True),
            'user_id': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request, location='cookies')
        self.certificate_id = parsed_args['certificate_id']
        self.user_id = parsed_args['user_id']

    def get_certificate_id(self):
        return self.certificate_id

    def get_task_id(self) -> int:
        return self.task_id

    def get_trigger_time(self) -> datetime:
        return self.trigger_time

    def get_user_id(self):
        return self.user_id


@wrap_response
def create_plan():
    params = HTTPParams()
    authentication_plugin = AuthenticationPlugin(
        certificate_repository=certificate_repository,
        params=params
    )
    use_case = CreatePlanUseCase(
        authentication_plugin=authentication_plugin,
        params=params,
        plan_repository=RepositoryFactory.plan(),
    )
    plan = use_case.run()
    return {
        'id': plan.id,
    }, 201

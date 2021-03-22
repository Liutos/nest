# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from ...app.use_case.list_plan import IParams, ListPlanUseCase
from ..repository import RepositoryFactory
from nest.web.authentication_plugin import AuthenticationPlugin, IParams as AuthenticationParams
from nest.web.certificate_repository import certificate_repository
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(AuthenticationParams, IParams):
    def __init__(self):
        args = {
            'page': fields.Int(missing=1),
            'per_page': fields.Int(missing=10),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self.page = parsed_args['page']
        self.per_page = parsed_args['per_page']
        args = {
            'certificate_id': fields.Int(required=True),
            'user_id': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request, location='cookies')
        self.certificate_id = parsed_args['certificate_id']
        self.user_id = parsed_args['user_id']

    def get_certificate_id(self) -> int:
        return self.certificate_id

    def get_page(self) -> int:
        return self.page

    def get_per_page(self) -> int:
        return self.per_page

    def get_user_id(self) -> int:
        return self.user_id


class ListPlanPresenter:
    def __init__(self, plans):
        self.plans = plans

    def format(self):
        plans = []
        for plan in self.plans:
            plans.append({
                'id': plan.id,
                'task_id': plan.task_id,
                'trigger_time': plan.trigger_time,
            })
        return {
            'plans': plans
        }


@wrap_response
def list_plan():
    params = HTTPParams()
    authentication_plugin = AuthenticationPlugin(
        certificate_repository=certificate_repository,
        params=params,
    )
    use_case = ListPlanUseCase(
        authentication_plugin=authentication_plugin,
        params=params,
        plan_repository=RepositoryFactory.plan(),
    )
    plans = use_case.run()
    presenter = ListPlanPresenter(plans)
    return presenter.format(), 200

# -*- coding: utf8 -*-
from typing import Union

from flask import request
from webargs import fields, validate

from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.list_plan import IParams, ListPlanUseCase
from nest.web.cookies_params import CookiesParams
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.plan import PlanPresenter


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'location_id': fields.Int(allow_none=True),
            'page': fields.Int(missing=1, validate=validate.Range(min=1)),
            'per_page': fields.Int(missing=10, validate=validate.Range(min=1)),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self.location_id = parsed_args.get('location_id')
        self.page = parsed_args['page']
        self.per_page = parsed_args['per_page']

    def get_location_id(self) -> Union[None, int]:
        return self.location_id

    def get_page(self) -> int:
        return self.page

    def get_per_page(self) -> int:
        return self.per_page

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


class ListPlanPresenter:
    def __init__(self, plans):
        self.plans = plans

    def format(self):
        plans = []
        for plan in self.plans:
            presenter = PlanPresenter(plan=plan)
            plans.append(presenter.format())
        return {
            'error': None,
            'result': plans,
            'status': 'success',
        }


@wrap_response
def list_plan(certificate_repository, repository_factory):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams()
    use_case = ListPlanUseCase(
        location_repository=repository_factory.location(),
        params=params,
        plan_repository=repository_factory.plan(),
    )
    plans = use_case.run()
    presenter = ListPlanPresenter(plans)
    return presenter.format(), 200

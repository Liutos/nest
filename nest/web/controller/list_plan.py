# -*- coding: utf8 -*-
from typing import List, Optional, Union

from flask import request
from webargs import fields, validate

from nest.app.use_case.list_plan import IParams, ListPlanUseCase
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.plan import PlanPresenter


class HTTPParams(IParams):
    def __init__(self, user_id: int):
        args = {
            'location_id': fields.Int(allow_none=True),
            'page': fields.Int(missing=1, validate=validate.Range(min=1)),
            'per_page': fields.Int(missing=10, validate=validate.Range(min=1)),
            'plan_ids': fields.DelimitedList(fields.Int, allow_none=True, missing=None),
            'task_ids': fields.DelimitedList(fields.Int, allow_none=True, missing=[]),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self._user_id = user_id
        self.location_id = parsed_args.get('location_id')
        self.page = parsed_args['page']
        self.per_page = parsed_args['per_page']
        self.plan_ids = parsed_args['plan_ids']
        self.task_ids = parsed_args['task_ids']

    def get_location_id(self) -> Union[None, int]:
        return self.location_id

    def get_page(self) -> int:
        return self.page

    def get_per_page(self) -> int:
        return self.per_page

    def get_plan_ids(self) -> Optional[List[int]]:
        return self.plan_ids

    def get_task_ids(self) -> List[int]:
        return self.task_ids

    def get_user_id(self) -> int:
        return self._user_id


class ListPlanPresenter:
    def __init__(self, plans, count: int):
        self.count = count
        self.plans = plans

    def format(self):
        plans = []
        for plan in self.plans:
            presenter = PlanPresenter(plan=plan)
            plans.append(presenter.format())
        return {
            'error': None,
            'result': {
                'count': self.count,
                'plans': plans,
            },
            'status': 'success',
        }


@wrap_response
@authenticate
def list_plan(repository_factory, user_id: int, **kwargs):
    params = HTTPParams(user_id)
    use_case = ListPlanUseCase(
        location_repository=repository_factory.location(),
        params=params,
        plan_repository=repository_factory.plan(),
    )
    plans, count = use_case.run()
    presenter = ListPlanPresenter(plans, count)
    return presenter.format(), 200

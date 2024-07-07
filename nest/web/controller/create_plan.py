# -*- coding: utf8 -*-
from datetime import datetime, timedelta
from typing import Set, Union

from flask import request
from webargs import fields

from nest.app.use_case.create_plan import CreatePlanUseCase, InvalidRepeatTypeError, IParams
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.plan import PlanPresenter


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'crontab': fields.Str(default=''),
            'duration': fields.Int(allow_none=True),
            'location_id': fields.Int(allow_none=True),
            'repeat_interval': fields.TimeDelta(allow_none=True),
            'repeat_type': fields.Str(allow_none=True),
            'task_id': fields.Int(required=True),
            'trigger_time': fields.DateTime('%Y-%m-%d %H:%M:%S', required=True),
            'visible_hours': fields.List(fields.Int, allow_none=True),
            'visible_wdays': fields.List(fields.Int, allow_none=True),
        }
        parsed_args = parser.parse(args, request)
        self._crontab = parsed_args.get('crontab')
        self.duration = parsed_args.get('duration')
        self.location_id = parsed_args.get('location_id')
        self.repeat_interval = parsed_args.get('repeat_interval')
        self.repeat_type = parsed_args.get('repeat_type')
        self.task_id = parsed_args['task_id']
        self.trigger_time = parsed_args['trigger_time']
        self.visible_hours = set(parsed_args.get('visible_hours') or [])
        self.visible_wdays = set(parsed_args.get('visible_wdays') or [])

    def get_crontab(self):
        return self._crontab

    def get_duration(self) -> Union[None, int]:
        return self.duration

    def get_location_id(self) -> Union[None, int]:
        return self.location_id

    def get_repeat_interval(self) -> Union[None, timedelta]:
        return self.repeat_interval

    def get_repeat_type(self) -> Union[None, str]:
        return self.repeat_type

    def get_task_id(self) -> int:
        return self.task_id

    def get_trigger_time(self) -> datetime:
        return self.trigger_time

    def get_visible_hours(self) -> Union[None, Set[int]]:
        return self.visible_hours

    def get_visible_wdays(self) -> Union[None, Set[int]]:
        return self.visible_wdays


@wrap_response
@authenticate
def create_plan(repository_factory, **kwargs):
    params = HTTPParams()
    use_case = CreatePlanUseCase(
        location_repository=repository_factory.location(),
        params=params,
        plan_repository=repository_factory.plan(),
        task_repository=repository_factory.task(),
    )
    try:
        plan = use_case.run()
        presenter = PlanPresenter(plan=plan)
        return {
            'error': None,
            'result': presenter.format(),
            'status': 'success',
        }, 201
    except InvalidRepeatTypeError as e:
        return {
            'error': {
                'message': '不支持的重复类型：{}'.format(e.repeat_type),
            },
            'result': None,
            'status': 'failure',
        }, 422

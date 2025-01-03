# -*- coding: utf8 -*-
from datetime import datetime, timedelta
from typing import Set, Tuple, Union, Optional

from flask import request
from webargs import fields

from nest.app.entity.plan import InvalidRepeatTypeError
from nest.app.use_case.change_plan import ChangePlanUseCase, PlanNotFoundError, IParams
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(IParams):
    def __init__(self, *, plan_id):
        self.plan_id = plan_id
        args = {
            'crontab': fields.Str(allow_none=True),
            'duration': fields.Int(allow_none=True),
            'location_id': fields.Int(allow_none=True),
            'repeat_interval': fields.TimeDelta(allow_none=True),
            'repeat_type': fields.Str(allow_none=True),
            'trigger_time': fields.DateTime('%Y-%m-%d %H:%M:%S'),
            'visible_hours': fields.List(fields.Int, allow_none=True),
            'visible_wdays': fields.List(fields.Int, allow_none=True),
        }
        parsed_args = parser.parse(args, request)
        self.parsed_args = parsed_args

    def get_crontab(self) -> Tuple[bool, Optional[str]]:
        return (
            'crontab' in self.parsed_args,
            self.parsed_args.get('crontab'),
        )

    def get_duration(self) -> Tuple[bool, Union[None, int]]:
        return (
            'duration' in self.parsed_args,
            self.parsed_args.get('duration'),
        )

    def get_location_id(self) -> Tuple[bool, Union[None, int]]:
        return (
            'location_id' in self.parsed_args,
            self.parsed_args.get('location_id'),
        )

    def get_plan_id(self) -> int:
        return self.plan_id

    def get_repeat_interval(self) -> Tuple[bool, Union[None, timedelta]]:
        return (
            'repeat_interval' in self.parsed_args,
            self.parsed_args.get('repeat_interval'),
        )

    def get_repeat_type(self) -> Tuple[bool, Union[None, str]]:
        found = 'repeat_type' in self.parsed_args
        return found, self.parsed_args.get('repeat_type')

    def get_trigger_time(self) -> Tuple[bool, Union[None, datetime]]:
        found = 'trigger_time' in self.parsed_args
        return found, self.parsed_args.get('trigger_time')

    def get_visible_hours(self) -> Tuple[bool, Union[None, Set[int]]]:
        found = 'visible_hours' in self.parsed_args
        return found, self.parsed_args.get('visible_hours')

    def get_visible_wdays(self) -> Tuple[bool, Union[None, Set[int]]]:
        found = 'visible_wdays' in self.parsed_args
        return found, self.parsed_args.get('visible_wdays')


@wrap_response
@authenticate
def change_plan(repository_factory, plan_id, **kwargs):
    params = HTTPParams(plan_id=plan_id)
    use_case = ChangePlanUseCase(
        location_repository=repository_factory.location(),
        params=params,
        plan_repository=repository_factory.plan(),
    )
    try:
        use_case.run()
        return {
            'error': None,
            'result': None,
            'status': 'success',
        }, 200
    except InvalidRepeatTypeError as e:
        return {
            'error': {
                'message': '不支持的重复类型：{}'.format(e.repeat_type),
            },
            'result': None,
            'status': 'failure',
        }, 200
    except PlanNotFoundError as e:
        return {
            'error': {
                'message': '找不到计划：{}'.format(e.plan_id),
            },
            'result': None,
            'status': 'failure',
        }, 200

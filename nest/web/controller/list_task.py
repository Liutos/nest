# -*- coding: utf8 -*-
import typing
from datetime import datetime
from typing import List, Optional, Tuple, Union

from flask import request
from webargs import fields, validate

from nest.app.entity.task import Task
from nest.app.use_case.list_task import IParams, ListTaskUseCase
from nest.infra.repository import MysqlUnitOfWork
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.task import Presenter


class HTTPParams(IParams):
    def __init__(self, user_id: int):
        args = {
            'keywords': fields.DelimitedList(fields.Str, missing=[]),
            'page': fields.Int(missing=1, validate=validate.Range(min=1)),
            'per_page': fields.Int(missing=10, validate=validate.Range(min=1)),
            'plan_trigger_time': fields.DelimitedList(fields.DateTime()),
            'status': fields.Int(),
            'task_ids': fields.DelimitedList(fields.Int()),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self._user_id = user_id
        self.count = parsed_args['per_page']
        self.keywords = parsed_args.get('keywords')
        self.plan_trigger_time = parsed_args.get('plan_trigger_time')
        self.start = (parsed_args['page'] - 1) * parsed_args['per_page']
        self.status = parsed_args.get('status')
        self.task_ids = parsed_args.get('task_ids')

    def get_count(self) -> int:
        return self.count

    def get_keywords(self) -> typing.List[str]:
        return self.keywords

    def get_plan_trigger_time(self) -> Optional[Tuple[datetime, datetime]]:
        if self.plan_trigger_time:
            return tuple(self.plan_trigger_time)
        return None

    def get_start(self) -> int:
        return self.start

    def get_status(self) -> Optional[int]:
        return self.status

    def get_task_ids(self) -> Union[None, List[int]]:
        return self.task_ids

    def get_user_id(self) -> int:
        return self._user_id


class ListPresenter:
    def __init__(self, *, tasks: List[Task]):
        self.tasks = tasks

    def build(self):
        tasks = [Presenter(task=task).build() for task in self.tasks]
        return {
            'error': None,
            'result': tasks,
            'status': 'success',
        }


@wrap_response
@authenticate
def list_task(repository_factory: MysqlUnitOfWork, user_id: int, **kwargs):
    params = HTTPParams(user_id)
    use_case = ListTaskUseCase(
        params=params,
        plan_repository=repository_factory.plan(),
        task_repository=repository_factory.task(),
    )
    tasks = use_case.run()
    return ListPresenter(tasks=tasks).build(), 200

# -*- coding: utf8 -*-
from typing import List, Optional, Union

from flask import request
from webargs import fields, validate

from nest.app.entity.task import Task
from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.list_task import IParams, ListTaskUseCase
from nest.web.cookies_params import CookiesParams
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'keyword': fields.Str(),
            'page': fields.Int(missing=1, validate=validate.Range(min=1)),
            'per_page': fields.Int(missing=10, validate=validate.Range(min=1)),
            'task_ids': fields.DelimitedList(fields.Int()),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self.count = parsed_args['per_page']
        self.keyword = parsed_args.get('keyword')
        self.start = (parsed_args['page'] - 1) * parsed_args['per_page']
        self.task_ids = parsed_args.get('task_ids')

    def get_count(self) -> int:
        return self.count

    def get_keyword(self) -> Optional[str]:
        return self.keyword

    def get_start(self) -> int:
        return self.start

    def get_task_ids(self) -> Union[None, List[int]]:
        return self.task_ids

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


class Presenter:
    def __init__(self, *, tasks: List[Task]):
        self.tasks = tasks

    def build(self):
        tasks = [{
            'brief': task.brief,
            'id': task.id,
            'keywords': task.keywords,
        } for task in self.tasks]
        return {
            'error': None,
            'result': tasks,
            'status': 'success',
        }


@wrap_response
def list_task(certificate_repository, repository_factory):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams()
    use_case = ListTaskUseCase(
        params=params,
        task_repository=repository_factory.task(),
    )
    tasks = use_case.run()
    return Presenter(tasks=tasks).build(), 200

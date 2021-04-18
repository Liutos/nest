# -*- coding: utf8 -*-
from typing import List

from flask import request
from webargs import fields, validate

from nest.app.entity.task import Task
from nest.app.use_case.list_task import IParams, ListTaskUseCase
from nest.web.authentication_plugin import (
    AuthenticationParamsMixin,
    AuthenticationPlugin,
)
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(AuthenticationParamsMixin, IParams):
    def __init__(self):
        args = {
            'page': fields.Int(missing=1, validate=validate.Range(min=1)),
            'per_page': fields.Int(missing=10, validate=validate.Range(min=1)),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self.count = parsed_args['per_page']
        self.start = (parsed_args['page'] - 1) * parsed_args['per_page']

    def get_count(self) -> int:
        return self.count

    def get_start(self) -> int:
        return self.start


class Presenter:
    def __init__(self, *, tasks: List[Task]):
        self.tasks = tasks

    def build(self):
        tasks = [{
            'brief': task.brief,
            'id': task.id,
        } for task in self.tasks]
        return {
            'error': None,
            'result': tasks,
            'status': 'success',
        }


@wrap_response
def list_task(certificate_repository, repository_factory):
    params = HTTPParams()
    authentication_plugin = AuthenticationPlugin(
        certificate_repository=certificate_repository,
        params=params,
    )
    use_case = ListTaskUseCase(
        authentication_plugin=authentication_plugin,
        certificate_repository=certificate_repository,
        params=params,
        task_repository=repository_factory.task(),
    )
    tasks = use_case.run()
    return Presenter(tasks=tasks).build(), 200

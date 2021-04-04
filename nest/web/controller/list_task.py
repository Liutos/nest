# -*- coding: utf8 -*-
from typing import List

from flask import request
from webargs import fields

from nest.app.entity.task import Task
from nest.app.use_case.list_task import IParams, ListTaskUseCase
from nest.web.authentication_plugin import AuthenticationPlugin, IParams as AuthenticationParams
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.repository import RepositoryFactory


class HTTPParams(AuthenticationParams, IParams):
    def __init__(self):
        args = {
            'count': fields.Int(missing=10),
            'start': fields.Int(missing=0),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self.count = parsed_args['count']
        self.start = parsed_args['start']
        args = {
            'certificate_id': fields.Str(required=True),
            'user_id': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request, location='cookies')
        self.certificate_id = parsed_args['certificate_id']
        self.user_id = parsed_args['user_id']

    def get_certificate_id(self) -> str:
        return self.certificate_id

    def get_count(self) -> int:
        return self.count

    def get_start(self) -> int:
        return self.start

    def get_user_id(self) -> int:
        return self.user_id


class Presenter:
    def __init__(self, *, tasks: List[Task]):
        self.tasks = tasks

    def build(self):
        tasks = [{
            'brief': task.brief,
            'id': task.id,
        } for task in self.tasks]
        return {
            'tasks': tasks,
        }


@wrap_response
def list_task(certificate_repository):
    params = HTTPParams()
    authentication_plugin = AuthenticationPlugin(
        certificate_repository=certificate_repository,
        params=params,
    )
    use_case = ListTaskUseCase(
        authentication_plugin=authentication_plugin,
        certificate_repository=certificate_repository,
        params=params,
        task_repository=RepositoryFactory.task(),
    )
    tasks = use_case.run()
    return Presenter(tasks=tasks).build(), 200

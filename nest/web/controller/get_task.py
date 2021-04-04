# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from ...app.use_case.get_task import IParams, GetTaskUseCase
from nest.app.entity.task import Task
from nest.web.authentication_plugin import AuthenticationPlugin, IParams as AuthenticationParams
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(AuthenticationParams, IParams):
    def __init__(self, *, task_id: str):
        self.task_id = int(task_id)
        args = {
            'certificate_id': fields.Str(required=True),
            'user_id': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request, location='cookies')
        self.certificate_id = parsed_args['certificate_id']
        self.user_id = parsed_args['user_id']

    def get_certificate_id(self) -> str:
        return self.certificate_id

    def get_task_id(self) -> int:
        return self.task_id

    def get_user_id(self) -> int:
        return self.user_id


class Presenter:
    def __init__(self, *, task: Task):
        self.task = task

    def build(self):
        return {
            'task': {
                'brief': self.task.brief,
                'id': self.task.id,
            }
        }


@wrap_response
def get_task(certificate_repository, id_, repository_factory):
    params = HTTPParams(task_id=id_)
    authentication_plugin = AuthenticationPlugin(
        certificate_repository=certificate_repository,
        params=params,
    )
    use_case = GetTaskUseCase(
        authentication_plugin=authentication_plugin,
        certificate_repository=certificate_repository,
        params=params,
        task_repository=repository_factory.task(),
    )
    task = use_case.run()
    presenter = Presenter(
        task=task,
    )
    return presenter.build(), 200

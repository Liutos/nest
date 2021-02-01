# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from ...app.use_case.list_task import IParams, ListTaskUseCase
from ..repository import RepositoryFactory
from nest.web.authentication_plugin import AuthenticationPlugin
from nest.web.certificate_repository import certificate_repository
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'count': fields.Int(missing=10),
            'start': fields.Int(missing=0),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self.count = parsed_args['count']
        self.start = parsed_args['start']
        args = {
            'certificate_id': fields.Int(required=True),
            'user_id': fields.Int(required=True),
        }
        parsed_args = parser.parse(args, request, location='cookies')
        self.certificate_id = parsed_args['certificate_id']
        self.user_id = parsed_args['user_id']

    def get_certificate_id(self) -> int:
        return self.certificate_id

    def get_count(self) -> int:
        return self.count

    def get_start(self) -> int:
        return self.start

    def get_user_id(self) -> int:
        return self.user_id


@wrap_response
def list_task():
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
    return {
        'tasks': tasks,
    }, 201

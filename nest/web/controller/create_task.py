# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from ...app.use_case.create_task import CreateTaskUseCase, IParams
from ..repository import RepositoryFactory
from nest.web.authentication_plugin import AuthenticationPlugin, IParams as AuthenticationParams
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(AuthenticationParams, IParams):
    def __init__(self):
        args = {
            'brief': fields.Str(required=True),
        }
        parsed_args = parser.parse(args, request)
        self.brief = parsed_args['brief']

    def get_brief(self):
        return self.brief

    def get_certificate_id(self) -> int:
        return request.cookies.get('certificate_id')

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


@wrap_response
def create_task(certificate_repository):
    params = HTTPParams()
    authentication_plugin = AuthenticationPlugin(
        certificate_repository=certificate_repository,
        params=params,
    )
    use_case = CreateTaskUseCase(
        authentication_plugin=authentication_plugin,
        certificate_repository=certificate_repository,
        params=params,
        task_repository=RepositoryFactory.task(),
    )
    task = use_case.run()
    return {
        'id': task.id,
    }, 201

# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from ...app.use_case.create_task import CreateTaskUseCase, IParams
from nest.web.authentication_plugin import (
    AuthenticationParamsMixin,
    AuthenticationPlugin,
)
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(AuthenticationParamsMixin, IParams):
    def __init__(self):
        args = {
            'brief': fields.Str(required=True),
        }
        parsed_args = parser.parse(args, request)
        self.brief = parsed_args['brief']

    def get_brief(self):
        return self.brief


@wrap_response
def create_task(certificate_repository, repository_factory):
    params = HTTPParams()
    authentication_plugin = AuthenticationPlugin(
        certificate_repository=certificate_repository,
        params=params,
    )
    use_case = CreateTaskUseCase(
        authentication_plugin=authentication_plugin,
        certificate_repository=certificate_repository,
        params=params,
        task_repository=repository_factory.task(),
    )
    task = use_case.run()
    return {
        'error': None,
        'result': {
            'id': task.id,
        },
        'status': 'success',
    }, 201

# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from nest.app.use_case.activate_user import (
    ActivateUserTestCase,
    IParams,
    IncorrectActivateCodeError,
    UserNotExistError
)
from nest.infra.repository import RepositoryFactory
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'activate_code': fields.Str(required=True),
            'email': fields.Str(required=True),
        }
        parsed_args = parser.parse(args, request)
        self.activate_code = parsed_args['activate_code']
        self.email = parsed_args['email']

    def get_email(self):
        return self.email

    def get_activate_code(self) -> str:
        return self.activate_code


@wrap_response
def activate_user(repository_factory: RepositoryFactory, **kwargs):
    try:
        params = HTTPParams()
        use_case = ActivateUserTestCase(
            params=params,
            user_repository=repository_factory.user(),
        )
        use_case.run()
        return {
            'error': None,
            'result': None,
            'status': 'success',
        }, 200
    except (IncorrectActivateCodeError, UserNotExistError):
        return {
            'error': {
                'message': '激活失败',
            },
            'result': None,
            'status': 'failure',
        }, 422

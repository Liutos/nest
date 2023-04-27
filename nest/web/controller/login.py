# -*- coding: utf8 -*-
from flask import make_response, request
from webargs import fields

from nest.app.use_case.login import IParams, LoginUseCase, PasswordError, UserNotActive
from nest.service.authenticate_service import AuthenticateService
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'email': fields.Str(required=True),
            'password': fields.Str(required=True),
        }
        parsed_args = parser.parse(args, request)
        self.email = parsed_args['email']
        self.password = parsed_args['password']

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password


@wrap_response
def login(certificate_repository, repository_factory):
    try:
        params = HTTPParams()
        authenticate_service = AuthenticateService(repository_factory.user())
        use_case = LoginUseCase(
            authenticate_service=authenticate_service,
            certificate_repository=certificate_repository,
            params=params,
        )
        certificate = use_case.run()
        response = make_response({
            'id': certificate.id,
        })
        response.set_cookie('certificate_id', str(certificate.id))
        response.set_cookie('user_id', str(certificate.user_id))
        return response
    except PasswordError:
        return {
            'error': {
                'code': 422,
                'message': '用户名或密码错误。',
            },
            'result': None,
            'status': 'failure',
        }, 422
    except UserNotActive:
        return {
            'error': {
                'code': 422,
                'message': '用户未激活。',
            },
            'result': None,
            'status': 'failure',
        }, 422

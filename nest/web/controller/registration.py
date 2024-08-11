# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from nest.app.use_case.registration import EmailOccupyError, IParams, RegistrationUseCase
from nest.infra.repository import MysqlUnitOfWork
from nest.infra.service_factory import ServiceFactory
from nest.web.handle_response import wrap_response
from nest.web.parser import parser


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'email': fields.Str(required=True),
            'nickname': fields.Str(required=True),
            'password': fields.Str(required=True),
        }
        parsed_args = parser.parse(args, request)
        self.email = parsed_args['email']
        self.nickname = parsed_args['nickname']
        self.password = parsed_args['password']

    def get_email(self):
        return self.email

    def get_nickname(self):
        return self.nickname

    def get_password(self):
        return self.password


@wrap_response
def register(repository_factory: MysqlUnitOfWork, service_factory: ServiceFactory, **kwargs):
    try:
        params = HTTPParams()
        use_case = RegistrationUseCase(
            location_repository=repository_factory.location(),
            mail_service=service_factory.mail(),
            params=params,
            user_repository=repository_factory.user(),
        )
        user = use_case.run()
        print('user', user)
        return {
            'error': None,
            'result': {
                'id': user.id,
            },
            'status': 'success',
        }, 201
    except EmailOccupyError:
        return {
            'error': {
                'code': 422,
                'message': '邮箱已被使用，请换一个邮箱注册。'
            },
            'result': None,
            'status': 'failure',
        }, 422

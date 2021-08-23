# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from ...app.use_case.registration import EmailOccupyError, IParams, RegistrationUseCase
from nest.infra.repository import RepositoryFactory
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
def register(repository_factory: RepositoryFactory, **kwargs):
    try:
        params = HTTPParams()
        use_case = RegistrationUseCase(
            location_repository=repository_factory.location(),
            params=params,
            user_repository=repository_factory.user(),
        )
        user = use_case.run()
        print('user', user)
        return {
            'id': user.id,
        }, 201
    except EmailOccupyError:
        return {
            'message': '邮箱已被使用，请换一个邮箱注册。'
        }, 422

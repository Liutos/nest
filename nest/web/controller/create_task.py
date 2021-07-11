# -*- coding: utf8 -*-
from typing import List

from flask import request
from webargs import fields

from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.create_task import CreateTaskUseCase, IParams
from nest.web.cookies_params import CookiesParams
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.task import Presenter


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'brief': fields.Str(required=True),
            'keywords': fields.List(fields.Str(), missing=[]),
        }
        parsed_args = parser.parse(args, request)
        self.brief = parsed_args['brief']
        self.keywords = parsed_args['keywords']

    def get_brief(self):
        return self.brief

    def get_keywords(self) -> List[str]:
        return self.keywords

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


@wrap_response
def create_task(certificate_repository, repository_factory):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams()
    use_case = CreateTaskUseCase(
        params=params,
        task_repository=repository_factory.task(),
    )
    task = use_case.run()
    return {
        'error': None,
        'result': Presenter(task=task).build(),
        'status': 'success',
    }, 201

# -*- coding: utf8 -*-
from typing import List

from flask import request
from webargs import fields

from nest.app.use_case.create_task import CreateTaskUseCase, IParams
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.task import Presenter


class HTTPParams(IParams):
    def __init__(self, user_id: int):
        args = {
            'brief': fields.Str(required=True),
            'detail': fields.Str(missing=''),
            'keywords': fields.List(fields.Str(), missing=[]),
        }
        parsed_args = parser.parse(args, request)
        self._detail = parsed_args['detail']
        self._user_id = user_id
        self.brief = parsed_args['brief']
        self.keywords = parsed_args['keywords']

    def get_brief(self):
        return self.brief

    def get_detail(self) -> str:
        return self._detail

    def get_keywords(self) -> List[str]:
        return self.keywords

    def get_user_id(self) -> int:
        return self._user_id


@wrap_response
@authenticate
def create_task(repository_factory, *, user_id: int, **kwargs):
    params = HTTPParams(user_id)
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

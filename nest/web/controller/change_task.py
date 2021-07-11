# -*- coding: utf8 -*-
from typing import Tuple

from flask import request
from webargs import fields

from nest.app.entity.certificate import ICertificateRepository
from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.change_task import (
    ChangeTaskUseCase,
    IParams,
)
from nest.infra.repository import RepositoryFactory
from nest.web.cookies_params import CookiesParams
from nest.web.parser import parser
from nest.web.presenter.task import Presenter


class HTTPParams(IParams):
    def __init__(self, *, task_id: str):
        args = {
            'brief': fields.Str(),
            'keywords': fields.List(fields.Str()),
            'status': fields.Int(),
        }
        self.parsed_args = parser.parse(args, request)
        self.task_id = int(task_id)

    def get_brief(self) -> Tuple[bool, str]:
        return 'brief' in self.parsed_args, self.parsed_args.get('brief')

    def get_keywords(self) -> Tuple[bool, str]:
        return 'keywords' in self.parsed_args, self.parsed_args.get('keywords')

    def get_status(self) -> Tuple[bool, int]:
        return 'status' in self.parsed_args, self.parsed_args.get('status')

    def get_task_id(self) -> int:
        return self.task_id

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


def change_task(
        certificate_repository: ICertificateRepository,
        id_: str,
        repository_factory: RepositoryFactory,
):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams(task_id=id_)
    use_case = ChangeTaskUseCase(
        params=params,
        task_repository=repository_factory.task(),
    )
    task = use_case.run()
    presenter = Presenter(
        task=task,
    )
    return {
        'error': None,
        'result': presenter.build(),
        'status': 'success',
    }, 200

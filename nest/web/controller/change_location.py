# -*- coding: utf8 -*-
from typing import Tuple

from flask import request
from webargs import fields

from nest.app.entity.certificate import ICertificateRepository
from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.change_location import (
    ChangeLocationUseCase,
    IParams,
)
from nest.infra.repository import RepositoryFactory
from nest.web.cookies_params import CookiesParams
from nest.web.parser import parser
from nest.web.presenter.location import LocationPresenter


class HTTPParams(IParams):
    def __init__(self, *, location_id: str):
        args = {
            'name': fields.Str(),
        }
        self.parsed_args = parser.parse(args, request)
        self.location_id = int(location_id)

    def get_name(self) -> Tuple[bool, str]:
        return 'name' in self.parsed_args, self.parsed_args.get('name')

    def get_location_id(self) -> int:
        return self.location_id

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


def change_location(
        certificate_repository: ICertificateRepository,
        id_: str,
        repository_factory: RepositoryFactory,
):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams(location_id=id_)
    use_case = ChangeLocationUseCase(
        location_repository=repository_factory.location(),
        params=params,
    )
    location = use_case.run()
    presenter = LocationPresenter(
        location=location,
    )
    return {
        'error': None,
        'result': presenter.format(),
        'status': 'success',
    }, 200

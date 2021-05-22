# -*- coding: utf8 -*-
from flask import request
from webargs import fields

from nest.app.entity.certificate import ICertificateRepository
from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.create_location import (
    CreateLocationUseCase,
    IParams,
)
from nest.infra.repository import RepositoryFactory
from nest.web.cookies_params import CookiesParams
from nest.web.parser import parser
from nest.web.presenter.location import LocationPresenter


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'name': fields.Str(required=True),
        }
        parsed_args = parser.parse(args, request)
        self.name = parsed_args['name']

    def get_name(self) -> str:
        return self.name

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


def create_location(certificate_repository: ICertificateRepository,
                    repository_factory: RepositoryFactory):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    use_case = CreateLocationUseCase(
        location_repository=repository_factory.location(),
        params=HTTPParams(),
    )
    location = use_case.run()
    presenter = LocationPresenter(location=location)
    return {
        'error': None,
        'result': presenter.format(),
        'status': 'success',
    }, 201

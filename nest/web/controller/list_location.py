# -*- coding: utf8 -*-
from typing import Union

from flask import request
from webargs import fields, validate

from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.list_location import IParams, ListLocationUseCase
from nest.web.cookies_params import CookiesParams
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.location import LocationPresenter


class HTTPParams(IParams):
    def __init__(self):
        args = {
            'name': fields.Str(allow_none=True),
            'page': fields.Int(missing=1, validate=validate.Range(min=1)),
            'per_page': fields.Int(missing=10, validate=validate.Range(min=1)),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self.name = parsed_args.get('name')
        self.page = parsed_args['page']
        self.per_page = parsed_args['per_page']

    def get_name(self) -> Union[None, str]:
        return self.name

    def get_page(self) -> int:
        return self.page

    def get_per_page(self) -> int:
        return self.per_page

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


class ListPlanPresenter:
    def __init__(self, locations):
        self.locations = locations

    def format(self):
        locations = []
        for location in self.locations:
            presenter = LocationPresenter(location=location)
            locations.append(presenter.format())
        return {
            'error': None,
            'result': locations,
            'status': 'success',
        }


@wrap_response
def list_location(certificate_repository, repository_factory):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams()
    use_case = ListLocationUseCase(
        location_repository=repository_factory.location(),
        params=params,
    )
    locations = use_case.run()
    presenter = ListPlanPresenter(locations)
    return presenter.format(), 200

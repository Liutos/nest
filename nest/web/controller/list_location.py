# -*- coding: utf8 -*-
from typing import List, Union

from flask import request
from webargs import fields, validate

from nest.app.use_case.list_location import IParams, ListLocationUseCase
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.parser import parser
from nest.web.presenter.location import LocationPresenter


class HTTPParams(IParams):
    def __init__(self, user_id: int):
        args = {
            'ids': fields.DelimitedList(fields.Int, allow_none=True),
            'name': fields.Str(allow_none=True),
            'page': fields.Int(missing=1, validate=validate.Range(min=1)),
            'per_page': fields.Int(missing=10, validate=validate.Range(min=1)),
        }
        parsed_args = parser.parse(args, request, location='querystring')
        self._user_id = user_id
        self.ids = parsed_args.get('ids')
        self.name = parsed_args.get('name')
        self.page = parsed_args['page']
        self.per_page = parsed_args['per_page']

    def get_ids(self) -> Union[None, List[int]]:
        return self.ids

    def get_name(self) -> Union[None, str]:
        return self.name

    def get_page(self) -> int:
        return self.page

    def get_per_page(self) -> int:
        return self.per_page

    def get_user_id(self) -> int:
        return self._user_id


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
@authenticate
def list_location(repository_factory, user_id: int, **kwargs):
    params = HTTPParams(user_id)
    use_case = ListLocationUseCase(
        location_repository=repository_factory.location(),
        params=params,
    )
    locations = use_case.run()
    presenter = ListPlanPresenter(locations)
    return presenter.format(), 200

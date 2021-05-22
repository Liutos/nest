# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.location import ILocationRepository, Location


class IParams(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class CreateLocationUseCase:
    def __init__(self, *, location_repository, params):
        assert isinstance(location_repository, ILocationRepository)
        assert isinstance(params, IParams)
        self.location_repository = location_repository
        self.params = params

    def run(self):
        params = self.params
        name = params.get_name()
        user_id = params.get_user_id()
        location = Location.new(
            name=name,
            user_id=user_id,
        )
        self.location_repository.add(location=location)
        return location

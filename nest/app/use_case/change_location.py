# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Tuple

from nest.app.entity.location import (
    AccessDeniedError,
    ILocationRepository,
    Location,
)


class IParams(ABC):
    @abstractmethod
    def get_location_id(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class LocationNotFoundError(Exception):
    def __init__(self, *, location_id: int):
        self.location_id = location_id


class ChangeLocationUseCase:
    def __init__(self, *, location_repository: ILocationRepository, params: IParams):
        self.location_repository = location_repository
        self.params = params

    def run(self) -> Location:
        params = self.params
        location_id = params.get_location_id()
        location = self.location_repository.get(id_=location_id)
        if location is None:
            raise LocationNotFoundError(location_id=location_id)

        if params.get_user_id() != location.user_id:
            raise AccessDeniedError()

        found, name = params.get_name()
        if found:
            location.name = name
        self.location_repository.add(location=location)
        return location

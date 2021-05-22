# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.location import ILocationRepository


class IParams(ABC):
    @abstractmethod
    def get_page(self) -> int:
        pass

    @abstractmethod
    def get_per_page(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class ListLocationUseCase:
    def __init__(self, *, location_repository, params):
        assert isinstance(location_repository, ILocationRepository)
        assert isinstance(params, IParams)
        self.location_repository = location_repository
        self.params = params

    def run(self):
        params = self.params
        page = params.get_page()
        per_page = params.get_per_page()
        user_id = params.get_user_id()
        location_repository = self.location_repository
        return location_repository.find(
            page=page,
            per_page=per_page,
            user_id=user_id,
        )

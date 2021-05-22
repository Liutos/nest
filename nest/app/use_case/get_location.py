# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.location import ILocationRepository


class IParams(ABC):
    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class AccessDeniedError(Exception):
    """用户无权访问给定地点的错误。"""
    pass


class GetLocationUseCase:
    def __init__(self, *, location_repository, params):
        assert isinstance(location_repository, ILocationRepository)
        assert isinstance(params, IParams)
        self.params = params
        self.plan_repository = location_repository

    def run(self):
        params = self.params
        location_id = params.get_id()
        user_id = params.get_user_id()
        location = self.plan_repository.get(id_=location_id)
        if user_id != location.user_id:
            raise AccessDeniedError()

        return location

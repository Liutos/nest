# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.location import (
    ILocationRepository,
)
from nest.app.entity.plan import IPlanRepository


class IParams(ABC):
    @abstractmethod
    def get_location_id(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


# TODO: 统一多个文件中的该异常。
class AccessDeniedError(Exception):
    pass


class LocationInUseError(Exception):
    """表示地点被某一计划所使用。"""
    def __init__(self, *, plan_id: int):
        self.plan_id = plan_id


class LocationNotFoundError(Exception):
    pass


class DeleteLocationUseCase:
    def __init__(self, *, location_repository: ILocationRepository,
                 params: IParams,
                 plan_repository: IPlanRepository):
        self.location_repository = location_repository
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        location_repository = self.location_repository
        location_id = self.params.get_location_id()
        location = location_repository.get(id_=location_id)
        if location is None:
            raise LocationNotFoundError()

        if self.params.get_user_id() != location.user_id:
            raise AccessDeniedError()

        plan_repository = self.plan_repository
        plans, _ = plan_repository.find_as_queue(
            location_ids=[location_id],
            user_id=self.params.get_user_id(),
        )
        if len(plans) > 0:
            raise LocationInUseError(plan_id=plans[0].id)

        location_repository.remove(id_=location_id)

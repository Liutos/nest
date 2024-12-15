# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Set, Tuple, Union, Optional

from nest.app.entity.location import ILocationRepository
from nest.app.entity.plan import (
    InvalidRepeatTypeError,
    IPlanRepository,
    Plan,
    UnchangeableError, REPEAT_TYPE_CRONTAB,
)


class IParams(ABC):
    @abstractmethod
    def get_crontab(self) -> Tuple[bool, Optional[str]]:
        pass

    @abstractmethod
    def get_duration(self) -> Tuple[bool, Union[None, int]]:
        pass

    @abstractmethod
    def get_location_id(self) -> Tuple[bool, Union[None, int]]:
        pass

    @abstractmethod
    def get_plan_id(self) -> int:
        pass

    @abstractmethod
    def get_repeat_interval(self) -> Tuple[bool, Union[None, timedelta]]:
        pass

    @abstractmethod
    def get_repeat_type(self) -> Tuple[bool, Union[None, str]]:
        pass

    @abstractmethod
    def get_trigger_time(self) -> Tuple[bool, Union[None, datetime]]:
        pass

    @abstractmethod
    def get_visible_hours(self) -> Tuple[bool, Union[None, Set[int]]]:
        pass

    @abstractmethod
    def get_visible_wdays(self) -> Tuple[bool, Union[None, Set[int]]]:
        pass


class LocationNotFoundError(Exception):
    def __init__(self, *, location_id):
        self.location_id = location_id


class PlanNotFoundError(Exception):
    def __init__(self, *, plan_id):
        self.plan_id = plan_id


class ChangePlanUseCase:
    def __init__(self, *, location_repository: ILocationRepository,
                 params, plan_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        self.location_repository = location_repository
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        params = self.params
        plan_id = params.get_plan_id()
        plan = self.plan_repository.find_by_id(plan_id)
        if plan is None:
            raise PlanNotFoundError(plan_id=plan_id)
        if not plan.is_changeable():
            raise UnchangeableError()

        # TODO: 如何优化这类重复代码？引入元编程之类的写法划算吗？
        found, crontab = params.get_crontab()
        if found:
            plan.crontab = crontab

        found, duration = params.get_duration()
        if found:
            plan.duration = duration
        found, location_id = params.get_location_id()
        if found:
            if location_id:
                location = self.location_repository.get(id_=location_id)
                if not location:
                    raise LocationNotFoundError(location_id=location_id)
            plan.location_id = location_id
        found, repeat_interval = params.get_repeat_interval()
        if found:
            plan.repeat_interval = repeat_interval

        if crontab:
            plan.repeat_type = REPEAT_TYPE_CRONTAB
        else:
            found, repeat_type = params.get_repeat_type()
            if found:
                if not Plan.is_valid_repeat_type(repeat_type):
                    raise InvalidRepeatTypeError(repeat_type)
                plan.repeat_type = repeat_type

        found, trigger_time = params.get_trigger_time()
        if found:
            plan.trigger_time = trigger_time
        found, visible_hours = params.get_visible_hours()
        if found:
            plan.visible_hours = visible_hours
        found, visible_wdays = params.get_visible_wdays()
        if found:
            plan.visible_wdays = visible_wdays
        self.plan_repository.add(plan)

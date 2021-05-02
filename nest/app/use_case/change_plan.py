# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Set, Tuple, Union

from nest.app.entity.plan import (
    InvalidRepeatTypeError,
    IPlanRepository,
    Plan,
)


class IParams(ABC):
    @abstractmethod
    def get_duration(self) -> Tuple[bool, Union[None, int]]:
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


class PlanNotFoundError(Exception):
    def __init__(self, *, plan_id):
        self.plan_id = plan_id


class ChangePlanUseCase:
    def __init__(self, *, params, plan_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        params = self.params
        plan_id = params.get_plan_id()
        plan = self.plan_repository.find_by_id(plan_id)
        if plan is None:
            raise PlanNotFoundError(plan_id=plan_id)

        # TODO: 如何优化这类重复代码？引入元编程之类的写法划算吗？
        found, duration = params.get_duration()
        if found:
            # TODO: 是否应当让duration成为一个property呢？还是用setter来做检查？
            plan.duration = duration
        found, repeat_interval = params.get_repeat_interval()
        if found:
            plan.repeat_interval = repeat_interval
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

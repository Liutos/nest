# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Set, Union

from nest.app.entity.plan import (
    InvalidRepeatTypeError,
    IPlanRepository,
    Plan,
)


class IParams(ABC):
    @abstractmethod
    def get_duration(self) -> Union[None, int]:
        pass

    @abstractmethod
    def get_repeat_interval(self) -> Union[None, timedelta]:
        pass

    @abstractmethod
    def get_repeat_type(self) -> Union[None, str]:
        pass

    @abstractmethod
    def get_task_id(self) -> int:
        pass

    @abstractmethod
    def get_trigger_time(self) -> datetime:
        pass

    @abstractmethod
    def get_visible_hours(self) -> Union[None, Set[int]]:
        pass

    @abstractmethod
    def get_visible_wdays(self) -> Union[None, Set[int]]:
        pass


class CreatePlanUseCase:
    def __init__(self, *, params, plan_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        params = self.params
        duration = params.get_duration()
        repeat_type = params.get_repeat_type()
        if repeat_type and not Plan.is_valid_repeat_type(repeat_type):
            raise InvalidRepeatTypeError(repeat_type)

        task_id = params.get_task_id()
        trigger_time = params.get_trigger_time()
        visible_hours = params.get_visible_hours()
        visible_wdays = params.get_visible_wdays()
        # TODO: 检查task_id是否能找到一个任务
        plan = Plan.new(
            task_id,
            trigger_time,
            duration=duration,
            repeat_interval=params.get_repeat_interval(),
            repeat_type=repeat_type,
            visible_hours=visible_hours,
            visible_wdays=visible_wdays,
        )
        self.plan_repository.add(plan)
        return self.plan_repository.find_by_id(plan.id)

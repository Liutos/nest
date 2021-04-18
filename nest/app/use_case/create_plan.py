# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Set, Union

from nest.app.entity.plan import (
    InvalidRepeatTypeError,
    IPlanRepository,
    Plan,
)
from .authentication_plugin import IAuthenticationPlugin


class IParams(ABC):
    @abstractmethod
    def get_duration(self) -> Union[None, int]:
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
    def __init__(self, *, authentication_plugin, params, plan_repository):
        assert isinstance(authentication_plugin, IAuthenticationPlugin)
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        self.authentication_plugin = authentication_plugin
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        self.authentication_plugin.authenticate()

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
            repeat_type=repeat_type,
            visible_hours=visible_hours,
            visible_wdays=visible_wdays,
        )
        self.plan_repository.add(plan)
        return plan

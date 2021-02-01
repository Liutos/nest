# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime

from ..entity.plan import IPlanRepository, Plan
from .authentication_plugin import IAuthenticationPlugin


class IParams(ABC):
    @abstractmethod
    def get_task_id(self) -> int:
        pass

    @abstractmethod
    def get_trigger_time(self) -> datetime:
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
        task_id = params.get_task_id()
        trigger_time = params.get_trigger_time()
        # TODO: 检查task_id是否能找到一个任务
        plan = Plan.new(task_id, trigger_time)
        self.plan_repository.add(plan)
        return plan

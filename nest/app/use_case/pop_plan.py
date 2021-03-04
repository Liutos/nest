# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime

from ..entity.plan import IPlanRepository
from .authentication_plugin import IAuthenticationPlugin


class IParams(ABC):
    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class PopPlanUseCase:
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
        size = params.get_size()
        user_id = params.get_user_id()
        plan_repository = self.plan_repository
        plans = plan_repository.find_as_queue(
            max_trigger_time=datetime.now(),
            page=1,
            per_page=size,
            user_id=user_id,
        )
        for plan in plans:
            plan_repository.remove(plan.id)
        return plans

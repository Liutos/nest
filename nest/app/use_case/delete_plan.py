# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.plan import IPlanRepository
from nest.app.use_case.authentication_plugin import IAuthenticationPlugin


class IParams(ABC):
    @abstractmethod
    def get_plan_id(self) -> int:
        pass


class DeletePlanUseCase:
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
        plan_id = params.get_plan_id()
        self.plan_repository.remove(plan_id)

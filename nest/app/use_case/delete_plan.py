# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.plan import IPlanRepository


class IParams(ABC):
    @abstractmethod
    def get_plan_id(self) -> int:
        pass


class DeletePlanUseCase:
    def __init__(self, *, params, plan_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        params = self.params
        plan_id = params.get_plan_id()
        self.plan_repository.remove(plan_id)

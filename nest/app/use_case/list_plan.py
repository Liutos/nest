# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from ..entity.plan import IPlanRepository
from .authentication_plugin import IAuthenticationPlugin


class IParams(ABC):
    @abstractmethod
    def get_page(self) -> int:
        pass

    @abstractmethod
    def get_per_page(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class ListPlanUseCase:
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
        page = params.get_page()
        per_page = params.get_per_page()
        user_id = params.get_user_id()
        plan_repository = self.plan_repository
        return plan_repository.find_as_queue(
            page=page,
            per_page=per_page,
            user_id=user_id,
        )

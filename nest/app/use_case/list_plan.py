# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from nest.app.entity.location import ILocationRepository
from nest.app.entity.plan import IPlanRepository, PlanStatus


class IParams(ABC):
    @abstractmethod
    def get_location_id(self) -> Optional[int]:
        pass

    @abstractmethod
    def get_page(self) -> int:
        pass

    @abstractmethod
    def get_per_page(self) -> int:
        pass

    @abstractmethod
    def get_plan_ids(self) -> Optional[List[int]]:
        pass

    @abstractmethod
    def get_task_ids(self) -> List[int]:
        """期望筛选结果中的计划来自于这些任务。"""
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class ListPlanUseCase:
    def __init__(self, *, location_repository: ILocationRepository,
                 params, plan_repository):
        assert isinstance(params, IParams)
        assert isinstance(plan_repository, IPlanRepository)
        self.location_repository = location_repository
        self.params = params
        self.plan_repository = plan_repository

    def run(self):
        params = self.params
        location_id = params.get_location_id()
        page = params.get_page()
        per_page = params.get_per_page()
        plan_ids = params.get_plan_ids()
        user_id = params.get_user_id()
        plan_repository = self.plan_repository
        location_ids = None
        if location_id:
            default_location = self.location_repository.get_default(user_id=user_id)
            location_ids = [
                default_location.id,
                location_id,
            ]
        return plan_repository.find_as_queue(
            location_ids=location_ids,
            page=page,
            per_page=per_page,
            plan_ids=plan_ids,
            status=PlanStatus.READY,
            task_ids=params.get_task_ids(),
            user_id=user_id,
        )

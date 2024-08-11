# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union

from nest.app.entity.plan import PlanStatus
from nest.app.use_case.base import IUnitOfWork


class IParams(ABC):
    @abstractmethod
    def get_location_id(self) -> Union[None, int]:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class PopPlanUseCase:
    def __init__(self, *, params,
                 repository_factory: IUnitOfWork):
        assert isinstance(params, IParams)
        self._repository_factory = repository_factory
        self.params = params

    def run(self):
        params = self.params
        location_id = params.get_location_id()
        size = params.get_size()
        user_id = params.get_user_id()
        plan_repository = self._repository_factory.plan()
        location_ids = None
        if location_id:
            default_location = self._repository_factory.location().get_default(user_id=user_id)
            location_ids = [
                default_location.id,
                location_id,
            ]
        plans, _ = plan_repository.find_as_queue(
            location_ids=location_ids,
            max_trigger_time=datetime.now(),
            page=1,
            per_page=size,
            status=PlanStatus.READY,
            user_id=user_id,
        )
        for plan in plans:
            self._repository_factory.begin()
            try:
                if plan.is_repeated():
                    next_plan = plan.rebirth()
                    plan_repository.add(next_plan)

                plan.terminate()
                plan_repository.add(plan)
                self._repository_factory.commit()
            except Exception:
                # TODO: 这里有办法改写为更具体的异常类型吗？
                self._repository_factory.rollback()
                raise

        now = datetime.now()
        plans = [plan for plan in plans if plan.is_visible(trigger_time=now)]
        return plans

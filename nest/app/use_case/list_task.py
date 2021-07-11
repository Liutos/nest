# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Tuple, Union

from nest.app.entity.plan import IPlanRepository, Plan
from nest.app.entity.task import ITaskRepository, TaskStatus


class IParams(ABC):
    @abstractmethod
    def get_count(self) -> int:
        pass

    @abstractmethod
    def get_keyword(self) -> Optional[str]:
        pass

    def get_plan_trigger_time(self) -> Optional[Tuple[datetime, datetime]]:
        raise NotImplementedError

    @abstractmethod
    def get_start(self) -> int:
        pass

    def get_status(self) -> Optional[int]:
        raise NotImplementedError

    @abstractmethod
    def get_task_ids(self) -> Union[None, List[int]]:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class ListTaskUseCase:
    def __init__(self, *, params,
                 plan_repository: IPlanRepository,
                 task_repository):
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.plan_repository = plan_repository
        self.task_repository = task_repository

    def run(self):
        # 以下是真正的业务逻辑
        params = self.params
        count = params.get_count()
        start = params.get_start()
        task_ids = params.get_task_ids()
        plans = self._find_plans()
        if plans is not None:
            task_ids = [plan.task_id for plan in plans]

        user_id = params.get_user_id()
        task_repository = self.task_repository
        tasks = task_repository.find(
            count=count,
            keyword=params.get_keyword(),
            start=start,
            status=params.get_status() and TaskStatus(params.get_status()),
            task_ids=task_ids,
            user_id=user_id,
        )
        return tasks

    def _find_plans(self) -> Optional[List[Plan]]:
        """找出给定时间内会触发、并且不重复的计划。

        如果没有指定时间，则不查找，返回None。
        """
        params = self.params
        trigger_time_range = params.get_plan_trigger_time()
        if trigger_time_range is None:
            return None
        plans, _ = self.plan_repository.find_as_queue(
            max_trigger_time=trigger_time_range[1],
            min_trigger_time=trigger_time_range[0],
            user_id=params.get_user_id(),
        )
        return [plan for plan in plans if not plan.repeat_type]

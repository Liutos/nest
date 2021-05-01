# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.task import ITaskRepository


class IParams(ABC):
    @abstractmethod
    def get_task_id(self) -> int:
        pass


class GetTaskUseCase:
    def __init__(self, *, params, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.task_repository = task_repository

    def run(self):
        # 以下是真正的业务逻辑
        params = self.params
        task_id = params.get_task_id()
        task_repository = self.task_repository
        task = task_repository.find_by_id(
            id_=task_id,
        )
        return task

# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.task import ITaskRepository, Task


class IParams(ABC):
    @abstractmethod
    def get_brief(self) -> str:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class CreateTaskUseCase:
    def __init__(self, *,
                 params, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.task_repository = task_repository

    def run(self):
        # 从这里开始才是正式的创建任务的逻辑
        params = self.params
        brief = params.get_brief()
        user_id = params.get_user_id()
        task = Task.new(brief, user_id)
        task_repository = self.task_repository
        task_repository.add(task)
        return task

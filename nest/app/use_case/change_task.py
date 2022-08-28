# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List, Tuple

from nest.app.entity.task import (
    AccessDeniedError,
    ITaskRepository,
    Task,
    TaskNotFoundError,
    TaskStatus,
)


class IParams(ABC):
    @abstractmethod
    def get_brief(self) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def get_detail(self) -> Tuple[bool, str]:
        """获取是否有输入 detail 参数，以及输入的值。"""
        pass

    @abstractmethod
    def get_keywords(self) -> Tuple[bool, List[str]]:
        pass

    def get_status(self) -> Tuple[bool, int]:
        raise NotImplementedError

    @abstractmethod
    def get_task_id(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class ChangeTaskUseCase:
    def __init__(self, *, params, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.task_repository = task_repository

    def run(self) -> Task:
        params = self.params
        task_id = params.get_task_id()
        task = self.task_repository.find_by_id(id_=task_id)
        if task is None:
            raise TaskNotFoundError(task_id=task_id)
        if params.get_user_id() != task.user_id:
            raise AccessDeniedError()
        found, brief = params.get_brief()
        if found:
            task.brief = brief
        found, detail = params.get_detail()
        if found:
            task.detail = detail

        found, keywords = params.get_keywords()
        if found:
            task.keywords = keywords
        found, status = params.get_status()
        if found:
            task.status = TaskStatus(status)
        self.task_repository.add(task)
        return self.task_repository.find_by_id(id_=task_id)

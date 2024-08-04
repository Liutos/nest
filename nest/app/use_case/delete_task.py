# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.task import (
    AccessDeniedError,
    TaskNotFoundError,
)
from nest.app.use_case.base import IRepositoryFactory


class IParams(ABC):
    @abstractmethod
    def get_task_id(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class DeleteTaskUseCase:
    def __init__(self, *, params: IParams,
                 repository_factory: IRepositoryFactory):
        self._repository_factory = repository_factory
        self.params = params

    def run(self):
        task_id = self.params.get_task_id()
        task = self._repository_factory.task().find_by_id(id_=task_id)
        if task is None:
            raise TaskNotFoundError(task_id=task_id)

        if self.params.get_user_id() != task.user_id:
            raise AccessDeniedError()

        plan_repository = self._repository_factory.plan()
        task_repository = self._repository_factory.task()
        self._repository_factory.begin()
        try:
            task_repository.remove(id_=task_id)
            plans = plan_repository.find_by_task_id(task_id=task_id)
            for plan in plans:
                plan_repository.remove(plan.id)

            self._repository_factory.commit()
        except Exception:
            self._repository_factory.rollback()
            raise

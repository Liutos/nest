# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.plan import IPlanRepository
from nest.app.entity.task import (
    AccessDeniedError,
    ITaskRepository,
    TaskNotFoundError,
)


class IParams(ABC):
    @abstractmethod
    def get_task_id(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class DeleteTaskUseCase:
    def __init__(self, *, params: IParams,
                 plan_repository: IPlanRepository, task_repository: ITaskRepository):
        self.params = params
        self.plan_repository = plan_repository
        self.task_repository = task_repository

    def run(self):
        task_id = self.params.get_task_id()
        task = self.task_repository.find_by_id(id_=task_id)
        if task is None:
            raise TaskNotFoundError(task_id=task_id)

        if self.params.get_user_id() != task.user_id:
            raise AccessDeniedError()

        plan_repository = self.plan_repository
        task_repository = self.task_repository
        task_repository.start_transaction(with_repository=[plan_repository])
        try:
            task_repository.remove(id_=task_id)
            plans = plan_repository.find_by_task_id(task_id=task_id)
            for plan in plans:
                plan_repository.remove(plan.id)
            task_repository.commit()
        except Exception as e:
            task_repository.rollback()
            raise e

# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from ..entity.task import ITaskRepository


class IParams(ABC):
    @abstractmethod
    def get_count(self) -> int:
        pass

    @abstractmethod
    def get_keyword(self) -> Optional[str]:
        pass

    @abstractmethod
    def get_start(self) -> int:
        pass

    @abstractmethod
    def get_task_ids(self) -> Union[None, List[int]]:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class ListTaskUseCase:
    def __init__(self, *, params, task_repository):
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.params = params
        self.task_repository = task_repository

    def run(self):
        # 以下是真正的业务逻辑
        params = self.params
        count = params.get_count()
        start = params.get_start()
        task_ids = params.get_task_ids()
        user_id = params.get_user_id()
        task_repository = self.task_repository
        tasks = task_repository.find(
            count=count,
            keyword=params.get_keyword(),
            start=start,
            task_ids=task_ids,
            user_id=user_id,
        )
        return tasks

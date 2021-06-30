# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List, Optional, Union


class Task:
    def __init__(self):
        self.brief = None
        self.id = None
        self.keywords: List[str] = []
        self.user_id = None

    @classmethod
    def new(cls, brief, user_id, *, keywords: List[str] = None):
        instance = Task()
        instance.brief = brief
        instance.keywords = keywords or []
        instance.user_id = user_id
        return instance


class ITaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def commit(self):
        """提交一个事务，保证前面所有操作的持久性。"""
        pass

    @abstractmethod
    def find(self, *, count,
             keyword: Optional[str] = None,
             start, user_id,
             task_ids: Union[None, List[int]] = None) -> [Task]:
        pass

    @abstractmethod
    def find_by_id(self, *, id_) -> Union[None, Task]:
        pass

    @abstractmethod
    def remove(self, *, id_: int):
        pass

    @abstractmethod
    def rollback(self):
        """回滚一个事务，保证事务前后数据的一致性。"""
        pass

    @abstractmethod
    def start_transaction(self, *, with_repository=None):
        """开始一个事务，保证后续一系列操作的原子性。

        如果with_repository不为空，则表示这些仓库的操作处于同一个事务中。
        """
        pass


class AccessDeniedError(Exception):
    """用户无权访问给定任务的错误。"""
    pass


class TaskNotFoundError(Exception):
    def __init__(self, *, task_id: int):
        self.task_id = task_id

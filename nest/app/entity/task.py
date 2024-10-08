# -*- coding: utf8 -*-
import typing
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Union

from nest.app.entity.plan import Plan


class TaskStatus(Enum):
    CREATED = 1
    FINISHED = 2
    CANCELLED = 3


class Task:
    def __init__(self):
        self.brief = None
        self.id = None
        self.detail: str = ''
        self.keywords: List[str] = []
        self.plans: List[Plan] = []
        self.status: Optional[TaskStatus] = None
        self.user_id = None

    # TODO: 方法名 new 是否需要调整为更具体的变体。
    @classmethod
    def new(cls, brief, user_id, *, detail: str = '', keywords: List[str] = None,
            plans: List[Plan] = None,
            status: Optional[TaskStatus] = None):
        """参数 keywords 和 plans 的实际默认值为空列表。为了避免 PyCharm 的警告只好写成 None。"""
        instance = Task()
        instance.brief = brief
        instance.detail = detail
        instance.keywords = keywords or []
        instance.plans = plans or []
        instance.status = status or TaskStatus.CREATED
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
    def find(self, *, count,
             keywords: typing.List[str] = None,
             start, status: Optional[TaskStatus] = None, user_id,
             task_ids: Union[None, List[int]] = None) -> [Task]:
        pass

    @abstractmethod
    def find_by_id(self, *, id_) -> Union[None, Task]:
        pass

    @abstractmethod
    def remove(self, *, id_: int):
        pass


class AccessDeniedError(Exception):
    """用户无权访问给定任务的错误。"""
    pass


class TaskNotFoundError(Exception):
    def __init__(self, *, task_id: int):
        self.task_id = task_id

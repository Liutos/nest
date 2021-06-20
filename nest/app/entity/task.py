# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List, Union


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
    def find(self, *, count, start, user_id,
             task_ids: Union[None, List[int]] = None) -> [Task]:
        pass

    @abstractmethod
    def find_by_id(self, *, id_) -> Union[None, Task]:
        pass

# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Union


class Task:
    def __init__(self):
        self.brief = None
        self.id = None
        self.user_id = None

    @classmethod
    def new(cls, brief, user_id):
        instance = Task()
        instance.brief = brief
        instance.user_id = user_id
        return instance


class ITaskRepository(ABC):
    @abstractmethod
    def add(self, task: Task):
        pass

    @abstractmethod
    def find(self, *, count, start, user_id) -> [Task]:
        pass

    @abstractmethod
    def find_by_id(self, *, id_) -> Union[None, Task]:
        pass

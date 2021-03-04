# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List


class Plan:
    def __init__(self):
        self.id = None
        self.task_id = None
        self.trigger_time = None

    @classmethod
    def new(cls, task_id, trigger_time):
        instance = Plan()
        instance.task_id = task_id
        instance.trigger_time = trigger_time
        return instance


class IPlanRepository(ABC):
    @abstractmethod
    def add(self, plan: Plan):
        pass

    @abstractmethod
    def find_as_queue(self, *, page: int, per_page: int, user_id: int, max_trigger_time=None) -> List[Plan]:
        pass

    @abstractmethod
    def remove(self, id_: int):
        pass

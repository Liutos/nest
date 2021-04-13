# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List


class IRepeater(ABC):
    @abstractmethod
    def compute_next_trigger_time(self) -> datetime:
        pass


class FixedIntervalRepeaterMixin(ABC):
    def __init__(self, *, last_trigger_time: datetime, repeat_interval):
        self.last_trigger_time = last_trigger_time
        self.repeat_interval = repeat_interval

    def compute_next_trigger_time(self) -> datetime:
        next_trigger_time = self.last_trigger_time
        now = datetime.now()
        while next_trigger_time.timestamp() < now.timestamp():
            next_trigger_time += self.get_interval()
        return next_trigger_time

    @abstractmethod
    def get_interval(self) -> timedelta:
        pass


class DailyRepeater(FixedIntervalRepeaterMixin, IRepeater):
    def get_interval(self) -> timedelta:
        return timedelta(days=1)


class HourRepeater(FixedIntervalRepeaterMixin, IRepeater):
    def get_interval(self) -> timedelta:
        return timedelta(hours=1)


class WeeklyRepeater(FixedIntervalRepeaterMixin, IRepeater):
    def get_interval(self) -> timedelta:
        return timedelta(days=7)


_TYPE_TO_REPEATER_CLASS = {
    'daily': DailyRepeater,
    'hourly': HourRepeater,
    'weekly': WeeklyRepeater,
}


class RepeaterFactory:
    @classmethod
    def get_repeater(cls, *, last_trigger_time, repeat_interval, repeat_type):
        repeater_class = _TYPE_TO_REPEATER_CLASS[repeat_type]
        return repeater_class(
            last_trigger_time=last_trigger_time,
            repeat_interval=repeat_interval,
        )


class Plan:
    def __init__(self):
        self.id = None
        self.repeat_type = None
        self.task_id = None
        self.trigger_time = None
        self.visible_hours = set([])
        self.visible_wdays = set([])

    @classmethod
    def new(cls, task_id, trigger_time, *, repeat_type=None, visible_hours=None, visible_wdays=None):
        instance = Plan()
        instance.repeat_type = repeat_type
        instance.task_id = task_id
        instance.trigger_time = trigger_time
        instance.visible_hours = visible_hours
        instance.visible_wdays = visible_wdays
        return instance

    def is_repeated(self):
        return not not self.repeat_type

    @classmethod
    def is_valid_repeat_type(cls, repeat_type):
        return repeat_type in _TYPE_TO_REPEATER_CLASS

    def is_visible(self, *, trigger_time: datetime):
        """
        判断该计划在给定时刻是否可见。
        """
        if len(self.visible_hours) > 0:
            hour = trigger_time.hour
            if hour not in self.visible_hours:
                return False
        if len(self.visible_wdays) > 0:
            weekday = trigger_time.weekday()
            if weekday not in self.visible_wdays:
                return False
        return True

    def rebirth(self):
        """
        生成下一个触发时间的计划。
        """
        repeater = RepeaterFactory.get_repeater(
            last_trigger_time=self.trigger_time,
            repeat_interval=None,
            repeat_type=self.repeat_type,
        )
        instance = Plan()
        instance.repeat_type = self.repeat_type
        instance.task_id = self.task_id
        instance.trigger_time = repeater.compute_next_trigger_time()
        return instance


class IPlanRepository(ABC):
    @abstractmethod
    def add(self, plan: Plan):
        pass

    @abstractmethod
    def find_as_queue(self, *, page: int, per_page: int, user_id: int, max_trigger_time=None) -> List[Plan]:
        pass

    @abstractmethod
    def find_by_id(self, id_: int) -> Plan:
        pass

    @abstractmethod
    def remove(self, id_: int):
        pass


class InvalidRepeatTypeError(Exception):
    def __init__(self, repeat_type):
        self.repeat_type = repeat_type

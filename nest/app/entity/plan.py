# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Union


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


class MonthlyRepeater(IRepeater):
    def __init__(self, *, last_trigger_time: datetime, repeat_interval):
        self.last_trigger_time = last_trigger_time
        self.repeat_interval = repeat_interval

    def compute_next_trigger_time(self) -> datetime:
        next_trigger_time = self.last_trigger_time
        now = datetime.now()
        # TODO: 循环的流程应当剥离到IRepeater的使用者中。
        while next_trigger_time.timestamp() < now.timestamp():
            next_trigger_time = self._compute_once(next_trigger_time)
        return next_trigger_time

    def _compute_once(self, last_trigger_time: datetime) -> datetime:
        # 去到下一个月的同一天。如果下个月没有这一天，就继续增加一个月。
        current_month = datetime.now().month
        if current_month in [3, 5, 7, 8, 10]:
            next_month_days = 30
        elif current_month in [2, 4, 6, 9, 11, 12]:
            next_month_days = 31
        elif self._is_leap_year():
            next_month_days = 29
        else:
            next_month_days = 27

        current_day = datetime.now().day
        if current_day <= next_month_days:
            if last_trigger_time.month == 12:
                return last_trigger_time.replace(
                    month=1,
                    year=last_trigger_time.year + 1,
                )
            else:
                return last_trigger_time.replace(
                    month=last_trigger_time.month + 1,
                )
        else:
            if last_trigger_time.month in [11, 12]:
                return last_trigger_time.replace(
                    month=(last_trigger_time.month + 2) % 12,
                    year=last_trigger_time.year + 1,
                )
            else:
                return last_trigger_time.replace(
                    month=last_trigger_time.month + 2,
                )

    def _is_leap_year(self) -> bool:
        """如果当前年份为闰年，就返回True。"""
        current_year = datetime.now().year
        if current_year % 4 != 0:
            return False
        if current_year % 100 == 0:
            return False
        return current_year % 400 == 0


class PeriodicallyRepeater(FixedIntervalRepeaterMixin, IRepeater):
    def get_interval(self) -> timedelta:
        return self.repeat_interval


class WeeklyRepeater(FixedIntervalRepeaterMixin, IRepeater):
    def get_interval(self) -> timedelta:
        return timedelta(days=7)


_TYPE_TO_REPEATER_CLASS = {
    'daily': DailyRepeater,
    'hourly': HourRepeater,
    'monthly': MonthlyRepeater,
    'periodically': HourRepeater,
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


class InvalidDurationError(Exception):
    pass


class RepeatIntervalMissingError(Exception):
    pass


class Plan:
    def __init__(self):
        self.duration = None
        self.id = None
        self.location_id = None
        self.repeat_interval = None
        self.repeat_type = None
        self.task_id = None
        self.trigger_time = None
        self.visible_hours = set([])
        self.visible_wdays = set([])

    @classmethod
    def new(cls, task_id, trigger_time, *,
            duration: Union[None, int] = None,
            location_id: Union[None, int] = None,
            repeat_interval: Union[None, timedelta] = None,
            repeat_type=None, visible_hours=None, visible_wdays=None):
        if isinstance(duration, int) and duration < 0:
            raise InvalidDurationError()
        if repeat_type == 'periodically' and not repeat_interval:
            raise RepeatIntervalMissingError()

        instance = Plan()
        instance.duration = duration
        instance.location_id = location_id
        instance.repeat_interval = repeat_interval
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
        return repeat_type is None or repeat_type in _TYPE_TO_REPEATER_CLASS

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
            repeat_interval=self.repeat_interval,
            repeat_type=self.repeat_type,
        )
        instance = Plan()
        instance.duration = self.duration
        instance.location_id = self.location_id
        instance.repeat_interval = self.repeat_interval
        instance.repeat_type = self.repeat_type
        instance.task_id = self.task_id
        instance.trigger_time = repeater.compute_next_trigger_time()
        instance.visible_hours = self.visible_hours
        instance.visible_wdays = self.visible_wdays
        return instance


class IPlanRepository(ABC):
    @abstractmethod
    def add(self, plan: Plan):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def commit(self):
        """提交一个事务，保证前面所有操作的持久性。"""
        pass

    @abstractmethod
    def find_as_queue(self, *, location_ids: Union[None, List[int]] = None,
                      max_trigger_time=None,
                      page: int, per_page: int, user_id: int) -> List[Plan]:
        pass

    @abstractmethod
    def find_by_id(self, id_: int) -> Plan:
        pass

    @abstractmethod
    def remove(self, id_: int):
        pass

    @abstractmethod
    def rollback(self):
        """回滚一个事务，保证事务前后数据的一致性。"""
        pass

    @abstractmethod
    def start_transaction(self):
        """开始一个事务，保证后续一系列操作的原子性。"""
        pass


class InvalidRepeatTypeError(Exception):
    def __init__(self, repeat_type):
        self.repeat_type = repeat_type

# -*- coding: utf8 -*-
import typing
from datetime import timedelta
from typing import List, Set, Union
import unittest

from nest.app.entity.location import Location
from nest.app.entity.plan import IPlanRepository, InvalidDurationError, Plan
from nest.app.entity.task import ITaskRepository, Task
from nest.app.use_case.create_plan import CreatePlanUseCase, IParams
from tests.use_case import EmptyLocationRepository


class MockLocationRepository(EmptyLocationRepository):
    def add(self, *, location: Location):
        pass

    def clear(self):
        pass

    def find(self, *, page: int, per_page: int, user_id: int):
        pass

    def get(self, *, id_: int) -> Union[None, Location]:
        pass

    def get_default(self, *, user_id: int) -> Union[None, Location]:
        pass


class MockParams(IParams):
    def __init__(self, *, duration: int):
        self.duration = duration

    def get_crontab(self) -> typing.Optional[str]:
        pass

    def get_duration(self) -> Union[None, int]:
        return self.duration

    def get_location_id(self) -> Union[None, int]:
        return 344

    def get_repeat_interval(self) -> Union[None, timedelta]:
        return None

    def get_repeat_type(self) -> str:
        return 'hourly'

    def get_task_id(self) -> int:
        return 1

    def get_trigger_time(self) -> int:
        return 1234567890

    def get_visible_hours(self) -> Union[None, Set[int]]:
        return None

    def get_visible_wdays(self) -> Union[None, Set[int]]:
        return None


class MockPlanRepository(IPlanRepository):
    def __init__(self):
        self.plan = None

    def add(self, plan: Plan):
        plan.id = 123
        self.plan = plan

    def clear(self):
        pass

    def find_as_queue(self, *, location_ids: Union[None, List[int]] = None,
                      max_trigger_time=None,
                      page: int, per_page: int, user_id=None) -> List[Plan]:
        pass

    def find_by_id(self, id_: int) -> Plan:
        return self.plan

    def find_by_task_id(self, *, task_id: int) -> List[Plan]:
        pass

    def remove(self, id_: int):
        pass


class MockTaskRepository(ITaskRepository):
    def add(self, task: Task):
        pass

    def clear(self):
        pass

    def find(self, *, count, keywords=None, start, status=None, user_id,
             task_ids: Union[None, List[int]] = None) -> [Task]:
        pass

    def find_by_id(self, *, id_) -> Union[None, Task]:
        pass

    def remove(self, *, id_: int):
        pass


def test_create():
    use_case = CreatePlanUseCase(
        location_repository=MockLocationRepository(),
        params=MockParams(duration=233),
        plan_repository=MockPlanRepository(),
        task_repository=MockTaskRepository(),
    )
    plan = use_case.run()
    assert plan
    assert plan.duration == 233
    assert plan.location_id == 344
    assert plan.id
    assert plan.repeat_type == 'hourly'
    assert plan.task_id == 1
    assert plan.trigger_time == 1234567890


class CreatePlanTestCase(unittest.TestCase):
    def test_create_with_negative_duration(self):
        use_case = CreatePlanUseCase(
            location_repository=MockLocationRepository(),
            params=MockParams(duration=-1),
            plan_repository=MockPlanRepository(),
            task_repository=MockTaskRepository(),
        )
        with self.assertRaises(InvalidDurationError):
            use_case.run()

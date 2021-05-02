# -*- coding: utf8 -*-
from datetime import timedelta
from typing import List, Set, Union

from nest.app.entity.plan import IPlanRepository, Plan
from nest.app.use_case.create_plan import CreatePlanUseCase, IParams


class MockParams(IParams):
    def get_duration(self) -> Union[None, int]:
        return 233

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

    def find_as_queue(self, *, page: int, per_page: int) -> List[Plan]:
        pass

    def find_by_id(self, id_: int) -> Plan:
        return self.plan

    def remove(self, id_: int):
        pass


def test_create():
    use_case = CreatePlanUseCase(
        params=MockParams(),
        plan_repository=MockPlanRepository()
    )
    plan = use_case.run()
    assert plan
    assert plan.duration == 233
    assert plan.id
    assert plan.repeat_type == 'hourly'
    assert plan.task_id == 1
    assert plan.trigger_time == 1234567890

# -*- coding: utf8 -*-
from datetime import datetime, timedelta
from typing import List, Optional, Set, Tuple, Union
import unittest

from nest.app.entity.location import ILocationRepository, Location
from nest.app.entity.plan import IPlanRepository, Plan, PlanStatus, UnchangeableError
from nest.app.use_case.change_plan import ChangePlanUseCase, IParams


class MockLocationRepository(ILocationRepository):
    def add(self, *, location: Location):
        pass

    def clear(self):
        pass

    def find(self, *, ids: Union[None, List[int]] = None,
             name: Union[None, str] = None, page: int, per_page: int, user_id: int):
        pass

    def get(self, *, id_: int) -> Union[None, Location]:
        pass

    def get_default(self, *, user_id: int) -> Union[None, Location]:
        pass


class MockParams(IParams):
    def get_duration(self) -> Tuple[bool, Optional[int]]:
        return False, None

    def get_location_id(self) -> Tuple[bool, Optional[int]]:
        return False, None

    def get_plan_id(self) -> int:
        pass

    def get_repeat_interval(self) -> Tuple[bool, Optional[timedelta]]:
        return False, None

    def get_repeat_type(self) -> Tuple[bool, Optional[str]]:
        return True, 'hourly'

    def get_trigger_time(self) -> Tuple[bool, int]:
        return True, 1234567890

    def get_visible_hours(self) -> Tuple[bool, Optional[Set[int]]]:
        return False, None

    def get_visible_wdays(self) -> Tuple[bool, Optional[Set[int]]]:
        return False, None


class MockPlanRepository(IPlanRepository):
    def __init__(self):
        self.plan = Plan()
        self.plan.terminate()

    def add(self, plan: Plan):
        pass

    def clear(self):
        pass

    def commit(self):
        pass

    def find_as_queue(self, *, location_ids: Union[None, List[int]] = None,
                      max_trigger_time=None,
                      min_trigger_time: datetime = None,
                      page: Optional[int] = None, per_page: Optional[int] = None,
                      status: PlanStatus = None,
                      user_id: int) -> List[Plan]:
        pass

    def find_by_id(self, id_: int) -> Plan:
        return self.plan

    def find_by_task_id(self, *, task_id: int) -> List[Plan]:
        pass

    def remove(self, id_: int):
        pass

    def rollback(self):
        pass

    def start_transaction(self):
        pass


class ChangePlanTestCase(unittest.TestCase):
    def test_with_terminated(self):
        """测试修改一个已终止的计划的场景。"""
        use_case = ChangePlanUseCase(
            location_repository=MockLocationRepository(),
            params=MockParams(),
            plan_repository=MockPlanRepository(),
        )
        with self.assertRaises(UnchangeableError):
            use_case.run()


if __name__ == '__main__':
    unittest.main(verbosity=2)

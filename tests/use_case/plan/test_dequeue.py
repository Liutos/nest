# -*- coding: utf8 -*-
from typing import List, Tuple, Union

from nest.app.entity.location import ILocationRepository, Location
from nest.app.entity.plan import IPlanRepository, Plan
from nest.app.use_case.pop_plan import IParams, PopPlanUseCase


class MockLocationRepository(ILocationRepository):
    def add(self, *, location: Location):
        pass

    def clear(self):
        pass

    def get(self, *, id_: int) -> Union[None, Location]:
        pass

    def get_default(self, *, user_id: int) -> Union[None, Location]:
        location = Location()
        location.id = 233
        return location

    def find(self, *, page: int, per_page: int, user_id: int):
        pass


class MockParams(IParams):
    def get_location_id(self) -> Union[None, int]:
        pass

    def get_size(self) -> int:
        return 1

    def get_user_id(self) -> int:
        return 1234567890


class MockPlanRepository(IPlanRepository):
    def add(self, plan: Plan):
        pass

    def clear(self):
        pass

    def commit(self):
        pass

    def find_as_queue(self, *, location_ids: Union[None, List[int]] = None,
                      max_trigger_time=None,
                      page: int, per_page: int, user_id=None) -> Tuple[List[Plan], int]:
        return [Plan()], 1

    def find_by_id(self, id_: int) -> Plan:
        pass

    def find_by_task_id(self, *, task_id: int) -> List[Plan]:
        pass

    def remove(self, id_: int):
        pass

    def rollback(self):
        pass

    def start_transaction(self):
        pass


def test_dequeue():
    use_case = PopPlanUseCase(
        location_repository=MockLocationRepository(),
        params=MockParams(),
        plan_repository=MockPlanRepository()
    )
    plans = use_case.run()
    assert plans
    assert len(plans) == 1

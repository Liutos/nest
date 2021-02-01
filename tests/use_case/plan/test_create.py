# -*- coding: utf8 -*-
from typing import List

from nest.app.entity.plan import IPlanRepository, Plan
from nest.app.use_case.authentication_plugin import IAuthenticationPlugin
from nest.app.use_case.create_plan import CreatePlanUseCase, IParams


class MockAuthenticationPlugin(IAuthenticationPlugin):
    def authenticate(self):
        pass


class MockParams(IParams):
    def get_task_id(self) -> int:
        return 1

    def get_trigger_time(self) -> int:
        return 1234567890


class MockPlanRepository(IPlanRepository):
    def add(self, plan: Plan):
        plan.id = 123

    def find_as_queue(self, *, page: int, per_page: int) -> List[Plan]:
        pass

    def remove(self, id_: int):
        pass


def test_create():
    use_case = CreatePlanUseCase(
        authentication_plugin=MockAuthenticationPlugin(),
        params=MockParams(),
        plan_repository=MockPlanRepository()
    )
    plan = use_case.run()
    assert plan
    assert plan.id
    assert plan.task_id == 1
    assert plan.trigger_time == 1234567890
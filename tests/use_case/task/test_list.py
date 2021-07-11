# -*- coding: utf8 -*-
from datetime import datetime
from typing import List, Optional, Union, Tuple

from nest.app.entity.plan import IPlanRepository, Plan, PlanStatus
from nest.app.entity.task import ITaskRepository, Task
from nest.app.use_case.list_task import IParams, ListTaskUseCase


class MockParams(IParams):
    def get_certificate_id(self) -> int:
        return 1001

    def get_count(self) -> int:
        return 1

    def get_keyword(self) -> Optional[str]:
        return None

    def get_plan_trigger_time(self) -> Optional[Tuple[datetime, datetime]]:
        pass

    def get_start(self) -> int:
        return 0

    def get_status(self) -> Optional[int]:
        pass

    def get_task_ids(self) -> Union[None, List[int]]:
        return None

    def get_user_id(self) -> int:
        return 2001


class MockPlanRepository(IPlanRepository):
    def add(self, plan: Plan):
        pass

    def clear(self):
        pass

    def commit(self):
        pass

    def find_as_queue(self, *, location_ids: Union[None, List[int]] = None, max_trigger_time=None,
                      min_trigger_time: datetime = None, page: Optional[int] = None, per_page: Optional[int] = None,
                      status: PlanStatus = None, user_id: int) -> Tuple[List[Plan], int]:
        pass

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


class MockTaskRepository(ITaskRepository):
    def add(self, task: Task):
        task.id = 3001

    def clear(self):
        pass

    def commit(self):
        pass

    def find(self, *, count, keyword=None, start, status=None, user_id,
             task_ids=None):
        return [{}]

    def find_by_id(self, *, id_) -> Union[None, Task]:
        pass

    def remove(self, *, id_: int):
        pass

    def rollback(self):
        pass

    def start_transaction(self, *, with_repository=None):
        pass


def test_create():
    use_case = ListTaskUseCase(
        params=MockParams(),
        plan_repository=MockPlanRepository(),
        task_repository=MockTaskRepository()
    )
    tasks = use_case.run()
    assert tasks
    assert isinstance(tasks, list)

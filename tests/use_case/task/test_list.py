# -*- coding: utf8 -*-
from typing import List, Union

from nest.app.entity.task import ITaskRepository, Task
from nest.app.use_case.list_task import IParams, ListTaskUseCase


class MockParams(IParams):
    def get_certificate_id(self) -> int:
        return 1001

    def get_count(self) -> int:
        return 1

    def get_start(self) -> int:
        return 0

    def get_task_ids(self) -> Union[None, List[int]]:
        return None

    def get_user_id(self) -> int:
        return 2001


class MockTaskRepository(ITaskRepository):
    def add(self, task: Task):
        task.id = 3001

    def clear(self):
        pass

    def find(self, *, count, start, user_id,
             task_ids=None):
        return [{}]

    def find_by_id(self, *, id_) -> Union[None, Task]:
        pass


def test_create():
    use_case = ListTaskUseCase(
        params=MockParams(),
        task_repository=MockTaskRepository()
    )
    tasks = use_case.run()
    assert tasks
    assert isinstance(tasks, list)

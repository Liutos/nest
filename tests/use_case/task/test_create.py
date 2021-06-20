# -*- coding: utf8 -*-
from typing import List, Union

from nest.app.entity.certificate import ICertificateRepository, Certificate
from nest.app.entity.task import ITaskRepository, Task
from nest.app.use_case.create_task import CreateTaskUseCase, IParams


class MockCertificateRepository(ICertificateRepository):
    def add(self, certificate: Certificate):
        pass

    def get_by_certificate_id(self, certificate_id: str) -> Certificate:
        certificate = Certificate()
        certificate.user_id = 2001
        return certificate

    def get_by_user_id(self, user_id: int) -> Certificate:
        pass


class MockParams(IParams):
    def get_brief(self) -> str:
        return 'Hello'

    def get_keywords(self) -> List[str]:
        return []

    def get_user_id(self) -> int:
        return 2001


class MockTaskRepository(ITaskRepository):
    def add(self, task: Task):
        task.id = 3001

    def clear(self):
        pass

    def find(self, *, count, keyword, start, user_id, task_ids=None):
        pass

    def find_by_id(self, *, id_) -> Union[None, Task]:
        pass


def test_create():
    use_case = CreateTaskUseCase(
        params=MockParams(),
        task_repository=MockTaskRepository()
    )
    task = use_case.run()
    assert task
    assert task.brief == 'Hello'
    assert isinstance(task.id, int)
    assert task.user_id == 2001

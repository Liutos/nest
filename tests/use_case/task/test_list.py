# -*- coding: utf8 -*-
from typing import Union

from nest.app.entity.certificate import ICertificateRepository, Certificate
from nest.app.entity.task import ITaskRepository, Task
from nest.app.use_case.authentication_plugin import IAuthenticationPlugin
from nest.app.use_case.list_task import IParams, ListTaskUseCase


class MockAuthenticationPlugin(IAuthenticationPlugin):
    def authenticate(self):
        pass


class MockCertificateRepository(ICertificateRepository):
    def add(self, certificate: Certificate):
        pass

    def get_by_certificate_id(self, certificate_id: int) -> Certificate:
        certificate = Certificate()
        certificate.user_id = 2001
        return certificate

    def get_by_user_id(self, user_id: int) -> Certificate:
        pass


class MockParams(IParams):
    def get_certificate_id(self) -> int:
        return 1001

    def get_count(self) -> int:
        return 1

    def get_start(self) -> int:
        return 0

    def get_user_id(self) -> int:
        return 2001


class MockTaskRepository(ITaskRepository):
    def add(self, task: Task):
        task.id = 3001

    def find(self, *, count, start, user_id):
        return [{}]

    def find_by_id(self, *, id_) -> Union[None, Task]:
        pass


def test_create():
    use_case = ListTaskUseCase(
        authentication_plugin=MockAuthenticationPlugin(),
        certificate_repository=MockCertificateRepository(),
        params=MockParams(),
        task_repository=MockTaskRepository()
    )
    tasks = use_case.run()
    assert tasks
    assert isinstance(tasks, list)

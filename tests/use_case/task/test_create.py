# -*- coding: utf8 -*-
from nest.app.entity.certificate import ICertificateRepository, Certificate
from nest.app.entity.task import ITaskRepository, Task
from nest.app.use_case.authentication_plugin import IAuthenticationPlugin
from nest.app.use_case.create_task import CreateTaskUseCase, IParams


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
    def get_brief(self) -> str:
        return 'Hello'

    def get_certificate_id(self) -> int:
        return 1001

    def get_user_id(self) -> int:
        return 2001


class MockTaskRepository(ITaskRepository):
    def add(self, task: Task):
        task.id = 3001

    def find(self, *, count, start, user_id):
        pass


def test_create():
    use_case = CreateTaskUseCase(
        authentication_plugin=MockAuthenticationPlugin(),
        certificate_repository=MockCertificateRepository(),
        params=MockParams(),
        task_repository=MockTaskRepository()
    )
    task = use_case.run()
    assert task
    assert task.brief == 'Hello'
    assert isinstance(task.id, int)
    assert task.user_id == 2001

# -*- coding: utf8 -*-
from ...app.use_case.get_task import IParams, GetTaskUseCase
from nest.app.entity.task import Task
from nest.web.authentication_plugin import (
    AuthenticationParamsMixin,
    AuthenticationPlugin,
)
from nest.web.handle_response import wrap_response


class HTTPParams(AuthenticationParamsMixin, IParams):
    def __init__(self, *, task_id: str):
        self.task_id = int(task_id)

    def get_task_id(self) -> int:
        return self.task_id


class Presenter:
    def __init__(self, *, task: Task):
        self.task = task

    def build(self):
        return {
            'error': None,
            'result': {
                'brief': self.task.brief,
                'id': self.task.id,
            },
            'status': 'success',
        }


@wrap_response
def get_task(certificate_repository, id_, repository_factory):
    params = HTTPParams(task_id=id_)
    authentication_plugin = AuthenticationPlugin(
        certificate_repository=certificate_repository,
        params=params,
    )
    use_case = GetTaskUseCase(
        authentication_plugin=authentication_plugin,
        certificate_repository=certificate_repository,
        params=params,
        task_repository=repository_factory.task(),
    )
    task = use_case.run()
    presenter = Presenter(
        task=task,
    )
    return presenter.build(), 200

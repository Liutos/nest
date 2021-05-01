# -*- coding: utf8 -*-
from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.get_task import IParams, GetTaskUseCase
from nest.app.entity.task import Task
from nest.web.cookies_params import CookiesParams
from nest.web.handle_response import wrap_response


class HTTPParams(IParams):
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
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams(task_id=id_)
    use_case = GetTaskUseCase(
        params=params,
        task_repository=repository_factory.task(),
    )
    task = use_case.run()
    presenter = Presenter(
        task=task,
    )
    return presenter.build(), 200

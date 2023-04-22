# -*- coding: utf8 -*-
from nest.app.use_case.get_task import IParams, GetTaskUseCase
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.presenter.task import Presenter


class HTTPParams(IParams):
    def __init__(self, *, task_id: str, user_id: int):
        self._user_id = user_id
        self.task_id = int(task_id)

    def get_task_id(self) -> int:
        return self.task_id


@wrap_response
@authenticate
def get_task(id_, repository_factory, user_id: int, **kwargs):
    params = HTTPParams(task_id=id_, user_id=user_id)
    use_case = GetTaskUseCase(
        params=params,
        task_repository=repository_factory.task(),
    )
    task = use_case.run()
    presenter = Presenter(
        task=task,
    )
    return {
        'error': None,
        'result': presenter.build(),
        'status': 'success',
    }, 200

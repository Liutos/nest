# -*- coding: utf8 -*-
from nest.app.use_case.delete_task import DeleteTaskUseCase, IParams
from nest.infra.repository import RepositoryFactory
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response


class HTTPParams(IParams):
    def __init__(self, *, task_id, user_id: int):
        self._user_id = user_id
        self.task_id = task_id

    def get_task_id(self) -> int:
        return self.task_id

    def get_user_id(self) -> int:
        return self._user_id


@wrap_response
@authenticate
def delete_task(id_, repository_factory: RepositoryFactory, user_id: int, **kwargs):
    use_case = DeleteTaskUseCase(
        params=HTTPParams(task_id=id_, user_id=user_id),
        repository_factory=repository_factory,
    )
    use_case.run()
    return {
        'error': None,
        'result': None,
        'status': 'success',
    }, 200

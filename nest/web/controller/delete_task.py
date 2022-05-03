# -*- coding: utf8 -*-
from flask import request

from nest.app.use_case.delete_task import DeleteTaskUseCase, IParams
from nest.infra.repository import RepositoryFactory
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response


class HTTPParams(IParams):
    def __init__(self, *, task_id):
        self.task_id = task_id

    def get_task_id(self) -> int:
        return self.task_id

    def get_user_id(self) -> int:
        return int(request.cookies.get('user_id'))


@wrap_response
@authenticate
def delete_task(id_, repository_factory: RepositoryFactory, **kwargs):
    use_case = DeleteTaskUseCase(
        params=HTTPParams(task_id=id_),
        plan_repository=repository_factory.plan(),
        task_repository=repository_factory.task(),
    )
    use_case.run()
    return {
        'error': None,
        'result': None,
        'status': 'success',
    }, 200

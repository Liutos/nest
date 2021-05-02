# -*- coding: utf8 -*-
from nest.app.use_case.authenticate import AuthenticateUseCase
from nest.app.use_case.delete_plan import DeletePlanUseCase, IParams
from nest.web.cookies_params import CookiesParams
from nest.web.handle_response import wrap_response


class HTTPParams(IParams):
    def __init__(self, *, plan_id):
        self.plan_id = plan_id

    def get_plan_id(self) -> int:
        return self.plan_id


@wrap_response
def delete_plan(certificate_repository, id_, repository_factory):
    authenticate_use_case = AuthenticateUseCase(
        certificate_repository=certificate_repository,
        params=CookiesParams(),
    )
    authenticate_use_case.run()

    params = HTTPParams(
        plan_id=id_,
    )
    use_case = DeletePlanUseCase(
        params=params,
        plan_repository=repository_factory.plan(),
    )
    use_case.run()
    return {
        'error': None,
        'result': None,
        'status': 'success',
    }, 200

# -*- coding: utf8 -*-
from nest.app.use_case.get_plan import GetPlanUseCase, IParams
from nest.web.authentication_plugin import (
    AuthenticationPlugin,
    AuthenticationParamsMixin,
)
from nest.web.handle_response import wrap_response
from nest.web.presenter.plan import PlanPresenter


class HTTPParams(AuthenticationParamsMixin, IParams):
    def __init__(self, *, plan_id):
        self.plan_id = plan_id

    def get_plan_id(self) -> int:
        return self.plan_id


@wrap_response
def get_plan(certificate_repository, id_, repository_factory):
    params = HTTPParams(plan_id=id_)
    use_case = GetPlanUseCase(
        authentication_plugin=AuthenticationPlugin(
            certificate_repository=certificate_repository,
            params=params,
        ),
        params=params,
        plan_repository=repository_factory.plan(),
    )
    plan = use_case.run()
    if plan is None:
        return {
            'error': None,
            'result': None,
            'status': 'success',
        }, 200
    presenter = PlanPresenter(plan=plan)
    return {
        'error': None,
        'result': presenter.format(),
        'status': 'success',
    }, 200

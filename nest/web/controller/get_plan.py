# -*- coding: utf8 -*-
from nest.app.use_case.get_plan import GetPlanUseCase, IParams
from nest.web.authenticate import authenticate
from nest.web.handle_response import wrap_response
from nest.web.presenter.plan import PlanPresenter


class HTTPParams(IParams):
    def __init__(self, *, plan_id):
        self.plan_id = plan_id

    def get_plan_id(self) -> int:
        return self.plan_id


@wrap_response
@authenticate
def get_plan(id_, repository_factory, **kwargs):
    params = HTTPParams(plan_id=id_)
    use_case = GetPlanUseCase(
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

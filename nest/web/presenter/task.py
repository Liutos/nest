# -*- coding: utf8 -*-
from nest.app.entity.task import Task
from nest.web.presenter.plan import PlanPresenter


class Presenter:
    def __init__(self, *, task: Task):
        self.task = task

    def build(self):
        return {
            'brief': self.task.brief,
            'detail': self.task.detail,
            'id': self.task.id,
            'keywords': self.task.keywords,
            'plans': list([PlanPresenter(plan=plan).format() for plan in self.task.plans]),
            'status': self.task.status.value,
        }

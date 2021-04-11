# -*- coding: utf8 -*-
from datetime import datetime

from nest.app.entity.plan import Plan


class PlanPresenter:
    def __init__(self, *, plan: Plan):
        self.plan = plan

    def format(self):
        trigger_time: datetime = self.plan.trigger_time
        return {
            'id': self.plan.id,
            'repeat_type': self.plan.repeat_type,
            'task_id': self.plan.task_id,
            'trigger_time': trigger_time.strftime('%Y-%m-%d %H:%M:%S'),
        }

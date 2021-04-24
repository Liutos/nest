# -*- coding: utf8 -*-
from datetime import datetime, timedelta
from typing import Union

from nest.app.entity.plan import Plan


class PlanPresenter:
    def __init__(self, *, plan: Plan):
        self.plan = plan

    def format(self):
        repeat_interval: Union[None, timedelta] = self.plan.repeat_interval
        trigger_time: datetime = self.plan.trigger_time
        return {
            'duration': self.plan.duration,
            'id': self.plan.id,
            'repeat_interval': repeat_interval and repeat_interval.total_seconds(),
            'repeat_type': self.plan.repeat_type,
            'task_id': self.plan.task_id,
            'trigger_time': trigger_time.strftime('%Y-%m-%d %H:%M:%S'),
            'visible_hours': list(self.plan.visible_hours),
            'visible_wdays': list(self.plan.visible_wdays),
        }

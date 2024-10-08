# -*- coding: utf8 -*-
from datetime import datetime, timedelta
from typing import Union

from nest.app.entity.plan import Plan


class PlanPresenter:
    def __init__(self, *, plan: Plan):
        self.plan = plan

    def format(self):
        repeat_interval: Union[None, int, timedelta] = self.plan.repeat_interval
        if repeat_interval is not None:
            repeat_interval = int(repeat_interval.total_seconds())

        trigger_time: datetime = self.plan.trigger_time
        return {
            'crontab': self.plan.crontab,
            'duration': self.plan.duration,
            'id': self.plan.id,
            'location_id': self.plan.location_id,
            'repeat_interval': repeat_interval,
            'repeat_type': self.plan.repeat_type,
            'repeating_description': self.plan.get_repeating_description(),
            'status': self.plan.status.value,
            'task_id': self.plan.task_id,
            'trigger_time': trigger_time.strftime('%Y-%m-%d %H:%M:%S'),
            'visible_hours': list(self.plan.visible_hours),
            'visible_hours_description': self.plan.get_visible_hours_description(),
            'visible_wdays': list(self.plan.visible_wdays),
            'visible_wdays_description': self.plan.get_visible_wdays_description(),
        }

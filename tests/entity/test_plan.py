# -*- coding: utf8 -*-
from datetime import datetime

from nest.app.entity.plan import Plan


def test_rebirth():
    trigger_time = datetime.now()
    plan = Plan.new(
        task_id=1,
        trigger_time=trigger_time,
        repeat_type='hourly'
    )
    rebirth_plan = plan.rebirth()
    assert rebirth_plan.repeat_type == 'hourly'
    assert rebirth_plan.task_id == 1
    assert rebirth_plan.trigger_time.timestamp() - trigger_time.timestamp() == 60 * 60

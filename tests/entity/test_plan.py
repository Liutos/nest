# -*- coding: utf8 -*-
from datetime import datetime, timedelta

from nest.app.entity.plan import Plan, WeeklyRepeater


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


def test_weekly_repeater():
    """
    测试周重复模式。
    """
    trigger_time = datetime.now()
    weekly_repeater = WeeklyRepeater(
        last_trigger_time=trigger_time,
        repeat_interval='weekly',
    )
    next_trigger_time = weekly_repeater.compute_next_trigger_time()
    diff = next_trigger_time - trigger_time
    assert diff.total_seconds() == timedelta(days=7).total_seconds()

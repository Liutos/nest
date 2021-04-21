# -*- coding: utf8 -*-
from datetime import datetime, timedelta

from nest.app.entity.plan import Plan, WeeklyRepeater


def test_rebirth():
    trigger_time = datetime.now()
    plan = Plan.new(
        duration=2,
        task_id=1,
        trigger_time=trigger_time,
        repeat_type='hourly',
        visible_hours=[1],
        visible_wdays=[6],
    )
    rebirth_plan = plan.rebirth()
    for attr, value in plan.__dict__.items():
        if attr in ['id', 'trigger_time']:
            continue
        assert getattr(rebirth_plan, attr) == getattr(plan, attr)
    assert rebirth_plan.trigger_time.timestamp() - trigger_time.timestamp() == 60 * 60


def test_visible_hours():
    """
    测试可见小时的判断逻辑。
    """
    plan = Plan()
    plan.visible_hours = {12, 22}
    trigger_time1 = datetime(2020, 3, 12, 22, 14)
    trigger_time2 = datetime(2021, 4, 13, 23, 15)
    assert plan.is_visible(trigger_time=trigger_time1)
    assert not plan.is_visible(trigger_time=trigger_time2)


def test_visible_wdays():
    """
    测试星期几可见的判断逻辑。
    """
    plan = Plan()
    plan.visible_wdays = {0, 4}
    trigger_time1 = datetime(2021, 4, 12)
    trigger_time2 = datetime(2021, 4, 13)
    assert plan.is_visible(trigger_time=trigger_time1)
    assert not plan.is_visible(trigger_time=trigger_time2)


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

# -*- coding: utf8 -*-
from datetime import datetime, timedelta

from nest.app.entity.plan import (
    EndOfMonthRepeater,
    MonthlyRepeater,
    PeriodicallyRepeater,
    Plan,
    WeeklyRepeater,
)


def test_end_of_month_repeater():
    """测试月末重复的模式。"""
    trigger_time = datetime(2021, 6, 17, 22, 38)
    repeater = EndOfMonthRepeater(
        last_trigger_time=trigger_time,
        repeat_interval='end_of_monthly',
    )
    next_trigger_time = repeater.compute_next_trigger_time()
    assert next_trigger_time.year == 2021
    assert next_trigger_time.month == 7
    assert next_trigger_time.day == 31


def test_monthly_repeater():
    """测试按月重复的模式。"""
    trigger_time = datetime(2021, 6, 16, 22, 36)
    repeater = MonthlyRepeater(
        last_trigger_time=trigger_time,
        repeat_interval='monthly',
    )
    next_trigger_time = repeater.compute_next_trigger_time()
    assert next_trigger_time.year == 2021
    assert next_trigger_time.month == 7
    assert next_trigger_time.day == 16


def test_periodically_repeater():
    """测试三天一次的重复模式。"""
    trigger_time = datetime.now()
    repeater = PeriodicallyRepeater(
        last_trigger_time=trigger_time,
        repeat_interval=timedelta(days=3),
    )
    next_trigger_time = repeater.compute_next_trigger_time()
    diff = next_trigger_time - trigger_time
    assert diff.total_seconds() == timedelta(days=3).total_seconds()


def test_rebirth():
    trigger_time = datetime.now()
    plan = Plan.new(
        duration=2,
        repeat_interval=timedelta(days=3),
        repeat_type='periodically',
        task_id=1,
        trigger_time=trigger_time,
        visible_hours={1},
        visible_wdays={6},
    )
    rebirth_plan = plan.rebirth()
    for attr, value in plan.__dict__.items():
        if attr in ['id', 'trigger_time']:
            continue
        assert getattr(rebirth_plan, attr) == getattr(plan, attr)
    assert rebirth_plan.trigger_time.timestamp() - trigger_time.timestamp() == 3 * 24 * 60 * 60


def test_repeating_description():
    plan = Plan.new(
        task_id=0,
        trigger_time=datetime.now(),
        repeat_interval=timedelta(days=13),
        repeat_type='periodically',
    )
    description = plan.get_repeating_description()
    assert description == '每13天'


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


def test_visible_hours_description():
    plan = Plan.new(
        task_id=0,
        trigger_time=datetime.now(),
        repeat_interval=timedelta(days=13),
        repeat_type='periodically',
        visible_hours={1, 2, 3, 5, 8, 13, 21},
    )
    description = plan.get_visible_hours_description()
    assert description == '1/2/3/5/8/13/21点可见'


def test_visible_wdays():
    """
    测试星期几可见的判断逻辑。
    """
    plan = Plan()
    plan.visible_wdays = {1, 5}
    trigger_time1 = datetime(2021, 4, 12)  # 周一
    trigger_time2 = datetime(2021, 4, 13)  # 周二
    assert plan.is_visible(trigger_time=trigger_time1)
    assert not plan.is_visible(trigger_time=trigger_time2)


def test_visible_wdays_description():
    plan = Plan.new(
        task_id=0,
        trigger_time=datetime.now(),
        repeat_interval=timedelta(days=13),
        repeat_type='periodically',
        visible_wdays={1, 2, 3, 5},
    )
    description = plan.get_visible_wdays_description()
    assert description == '星期1/2/3/5可见'


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

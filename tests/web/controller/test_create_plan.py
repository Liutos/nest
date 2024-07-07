# -*- coding: utf8 -*-
import datetime
import unittest
from typing import List

from flask import Response

from nest.app.use_case import create_task
from nest.web import main
from tests.web import helper
from tests.web.user_helper import EMAIL, PASSWORD, register_user


class CreateTaskParams(create_task.IParams):
    def __init__(self, user_id):
        self._user_id = user_id

    def get_brief(self) -> str:
        return 'This is brief.'

    def get_detail(self) -> str:
        return 'This is detail.'

    def get_keywords(self) -> List[str]:
        return []

    def get_user_id(self) -> int:
        return self._user_id


class PlanTestCase(unittest.TestCase):
    """与计划有关的单测用例。"""
    _plan_id = None
    _task_id = None

    def clear_database(self):
        self.plan_repository.clear()
        self.task_repository.clear()
        self.user_repository.clear()

    def setUp(self) -> None:
        self.location_repository = helper.location_repository
        self.plan_repository = helper.plan_repository
        self.task_repository = helper.task_repository
        self.user_repository = helper.user_repository

        self.clear_database()
        user_id = register_user(self.location_repository, self.user_repository)
        # 创建任务。
        params = CreateTaskParams(user_id)
        task = create_task.CreateTaskUseCase(
            params=params,
            task_repository=helper.task_repository,
        ).run()
        self._task_id = task.id

    def tearDown(self) -> None:
        self.clear_database()

    def test_create_crontab(self):
        """测试创建一个按照 crontab 语法来周期性提醒的场景。"""
        with main.create_app().test_client() as client:
            client.post('/user/login', json={
                'email': EMAIL,
                'password': PASSWORD,
            })
            crontab = '*/5 * * * *'
            rv: Response = client.post('/plan', json={
                'crontab': crontab,
                'task_id': self._task_id,
                'trigger_time': '2024-07-07 14:24:00',
            })
            print('rv.get_data()', rv.get_data())
            self.assertEqual(rv.status_code, 201)
            data = rv.get_json()
            print('data', data)
            result = data['result']
            self.assertEqual(result['repeating_description'], crontab)
            plan_id = result['id']

        # 计算出这个提醒下一个被触发的时刻。
        plan = self.plan_repository.find_by_id(plan_id)
        self.assertIsNotNone(plan)
        next_trigger_time = plan.get_next_trigger_time()
        self.assertIsInstance(next_trigger_time, datetime.datetime)
        # 手动计算出下一个"5 分钟的倍数"的时刻。
        now = datetime.datetime.now()
        current_minutes = now.minute
        times = current_minutes // 5
        next_minutes = (times + 1) * 5
        target = (now + datetime.timedelta(minutes=(next_minutes - current_minutes))).replace(
            microsecond=0,
            second=0,
        )

        self.assertEqual(next_trigger_time, target)


if __name__ == '__main__':
    unittest.main(failfast=True, verbosity=2)

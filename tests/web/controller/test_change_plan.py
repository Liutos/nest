# -*- coding: utf8 -*-
import typing
from datetime import datetime, timedelta
import unittest
from typing import List, Union, Set

from flask import Response

from nest.app.use_case import create_task, create_plan
from nest.web import main
from tests.web import helper
from tests.web.user_helper import EMAIL, PASSWORD, register_user


class CreatePlanParams(create_plan.IParams):
    def __init__(self, task_id):
        self._task_id = task_id

    def get_crontab(self) -> typing.Optional[str]:
        pass

    def get_duration(self) -> Union[None, int]:
        return None

    def get_location_id(self) -> Union[None, int]:
        return None

    def get_repeat_interval(self) -> Union[None, timedelta]:
        return None

    def get_repeat_type(self) -> Union[None, str]:
        return None

    def get_task_id(self) -> int:
        return self._task_id

    def get_trigger_time(self) -> datetime:
        return datetime.now()

    def get_visible_hours(self) -> Union[None, Set[int]]:
        return set([])

    def get_visible_wdays(self) -> Union[None, Set[int]]:
        return set([])


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
        # 创建计划。
        create_plan_params = CreatePlanParams(task.id)
        plan = create_plan.CreatePlanUseCase(
            location_repository=helper.location_repository,
            params=create_plan_params,
            plan_repository=helper.plan_repository,
            task_repository=helper.task_repository,
        ).run()
        self._plan_id = plan.id
        # 终止计划——调用计划的 terminate 方法并保存即可。
        plan.terminate()
        helper.plan_repository.add(plan)

    def tearDown(self) -> None:
        self.clear_database()

    def test_unchangeable_error(self):
        """测试通过接口修改一个已经无法修改的计划的场景。"""
        with main.create_app().test_client() as client:
            client.post('/user/login', json={
                'email': EMAIL,
                'password': PASSWORD,
            })
            rv: Response = client.patch(f'/plan/{self._plan_id}', json={
                'trigger_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            print('rv.get_data()', rv.get_data())
            self.assertEqual(rv.status_code, 400)
            data = rv.get_json()
            self.assertIn('error', data)
            self.assertIn('message', data['error'])
            self.assertGreater(len(data['error']['message']), 0)

    def clear_database(self):
        self.plan_repository.clear()
        self.task_repository.clear()
        self.user_repository.clear()

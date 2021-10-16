# -*- coding: utf8 -*-
from datetime import datetime
import time
import unittest

from nest.app.entity.plan import PlanStatus
from nest.app.entity.task import TaskStatus
from nest.repository.location import DatabaseLocationRepository
from nest.repository.plan import DatabasePlanRepository
from nest.repository.task import DatabaseTaskRepository
from nest.repository.user import DatabaseUserRepository
from nest.web import main
from tests.web.user_helper import (
    EMAIL,
    PASSWORD,
    register_user,
)
from tests.web.helper import (
    location_repository,
    mysql_connection,
    plan_repository,
    task_repository,
    user_repository,
)


class PopPlanTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.location_repository = DatabaseLocationRepository(
            connection=mysql_connection,
        )
        self.plan_repository = DatabasePlanRepository(
            connection=mysql_connection,
        )
        self.task_repository = DatabaseTaskRepository(
            connection=mysql_connection,
        )
        self.user_repository = DatabaseUserRepository(
            connection=mysql_connection,
        )
        self.clear_database()
        register_user(self.location_repository, self.user_repository)
        print('初始化完毕')

    def tearDown(self) -> None:
        self.clear_database()
        print('清理数据库')

    def test_create_task(self):
        with main.app.test_client() as client:
            client.post('/user/login', json={
                'email': 'foobar.bef@gmail.com',
                'password': 'def',
            })
            # 创建任务以便联表查询
            rv = client.post('/task', json={
                'brief': 'test',
            })
            json_data = rv.get_json()
            assert json_data['result']['id']
            task_id = json_data['result']['id']

            now = datetime.now()
            time.sleep(1)
            rv = client.post('/plan', json={
                'repeat_type': 'hourly',
                'task_id': task_id,
                'trigger_time': now.strftime('%Y-%m-%d %H:%M:%S'),
            })
            json_data = rv.get_json()
            self.assertEqual(json_data['status'], 'success')
            assert json_data['result']['id']
            self.assertIsInstance(json_data['result']['id'], int)
            plan_id = json_data['result']['id']
            self.assertEqual(json_data['result']['status'], PlanStatus.READY.value)

            rv = client.post('/plan/pop', json={
                'size': 1,
            })
            json_data = rv.get_json()
            print('json_data', json_data)
            self.assertEqual(json_data['status'], 'success')
            plans = json_data['result']
            self.assertIsInstance(plans, list)
            self.assertEqual(len(plans), 1)
            plan = plans[0]
            self.assertEqual(plan['id'], plan_id)

            rv = client.get('/plan/{}'.format(plan_id))
            json_data = rv.get_json()
            plan = json_data['result']
            self.assertEqual(plan['status'], PlanStatus.TERMINATED.value)

    def clear_database(self):
        self.plan_repository.clear()
        self.task_repository.clear()
        self.user_repository.clear()


class PopFinishedTaskPlanTestCase(unittest.TestCase):
    """测试任务已完成，不再需要弹出计划的情况。"""
    def setUp(self) -> None:
        self.clear_database()
        register_user(location_repository, user_repository)

    def tearDown(self) -> None:
        self.clear_database()

    def test_it(self):
        with main.app.test_client() as client:
            client.post('/user/login', json={
                'email': EMAIL,
                'password': PASSWORD,
            })

            rv = client.post('/task', json={
                'brief': 'test',
            })
            json_data = rv.get_json()
            assert json_data['result']['id']
            task_id = json_data['result']['id']

            now = datetime.now()
            time.sleep(1)
            client.post('/plan', json={
                'repeat_type': 'hourly',
                'task_id': task_id,
                'trigger_time': now.strftime('%Y-%m-%d %H:%M:%S'),
            })

            rv = client.patch('/task/{}'.format(task_id), json={
                'status': TaskStatus.FINISHED.value,
            })
            json_data = rv.get_json()
            self.assertEqual(json_data['status'], 'success')

            rv = client.post('/plan/pop', json={
                'size': 1,
            })
            json_data = rv.get_json()
            print('json_data', json_data)
            self.assertEqual(json_data['status'], 'success')
            plans = json_data['result']
            self.assertEqual(len(plans), 0)

    def clear_database(self):
        plan_repository.clear()
        task_repository.clear()
        user_repository.clear()

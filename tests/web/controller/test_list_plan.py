# -*- coding: utf8 -*-
from datetime import datetime
import time
import unittest

from nest.web import main
from tests.web import helper
from tests.web.user_helper import EMAIL, PASSWORD, register_user


class ListPlanTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.location_repository = helper.location_repository
        self.plan_repository = helper.plan_repository
        self.task_repository = helper.task_repository
        self.user_repository = helper.user_repository

        self.clear_database()
        register_user(self.location_repository, self.user_repository)

    def tearDown(self) -> None:
        self.clear_database()

    def test_list_plan(self):
        """测试列出一个指定计划的场景。"""
        with main.create_app().test_client() as client:
            client.post('/user/login', json={
                'email': EMAIL,
                'password': PASSWORD,
            })

            rv = client.post('/task', json={
                'brief': 'test',
            })
            self.assertEqual(rv.status_code, 201)
            json_data = rv.get_json()
            self.assertTrue(json_data['result']['id'])
            task_id = json_data['result']['id']

            # 创建两个提醒，并且只取其中的一个。
            now = datetime.now()
            rv = client.post('/plan', json={
                'repeat_type': 'hourly',
                'task_id': task_id,
                'trigger_time': now.strftime('%Y-%m-%d %H:%M:%S'),
            })
            self.assertEqual(rv.status_code, 201)
            json_data = rv.get_json()
            plan_id: int = json_data['result']['id']  # 这个是稍后要获取的计划的ID
            time.sleep(1)
            now = datetime.now()
            client.post('/plan', json={
                'repeat_type': 'hourly',
                'task_id': task_id,
                'trigger_time': now.strftime('%Y-%m-%d %H:%M:%S'),
            })

            # get方法所支持的参数参见[这里](https://werkzeug.palletsprojects.com/en/2.0.x/test/#werkzeug.test.EnvironBuilder)
            rv = client.get('/plan', query_string={
                'plan_ids': ','.join(map(str, [plan_id])),
            })
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.get_json()['status'], 'success')
            result = rv.get_json()['result']
            self.assertEqual(len(result['plans']), 1)
            self.assertEqual(result['plans'][0]['id'], plan_id)

    def clear_database(self):
        self.plan_repository.clear()
        self.task_repository.clear()
        self.user_repository.clear()

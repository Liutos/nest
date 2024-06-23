# -*- coding: utf8 -*-
# 测试任务列表的接口
from datetime import datetime, timedelta
import unittest

import flask.wrappers

from nest.web import main
from tests.web import helper
from tests.web.user_helper import EMAIL, PASSWORD, register_user


class ListTaskTestCase(unittest.TestCase):
    def setUp(self) -> None:
        location_repository = helper.location_repository
        task_repository = helper.task_repository
        user_repository = helper.user_repository
        self.task_repository = task_repository
        self.user_repository = user_repository

        self.clear_database()
        register_user(location_repository, user_repository)

    def tearDown(self) -> None:
        self.clear_database()

    def test_list_task(self):
        # 先登录，再创建任务，再创建提醒，最后查询列表。
        with main.create_app().test_client() as client:
            client.post('/user/login', json={
                'email': EMAIL,
                'password': PASSWORD,
            })

            rv = client.post('/task', json={
                'brief': 'Hello, nest!',
                'keywords': [
                    'hello',
                    'nest',
                ],
            })
            self.assertEqual(rv.status_code, 201)
            json_data = rv.get_json()
            task_id = json_data['result']['id']

            now = datetime.now() + timedelta(days=1)
            trigger_time = now.strftime('%Y-%m-%d %H:%M:%S')
            rv = client.post('/plan', json={
                'task_id': task_id,
                'trigger_time': trigger_time,
            })
            self.assertEqual(rv.status_code, 201)

            rv: flask.wrappers.Response = client.get('/task', query_string={
                'keywords': ','.join(['goodbye', 'hello', 'nest']),
            })
            self.assertEqual(rv.status_code, 200)
            json_data = rv.get_json()
            self.assertIn('result', json_data)
            tasks = json_data['result']
            self.assertEqual(len(tasks), 1)
            task: dict = tasks[0]
            self.assertIn('plans', task)
            self.assertEqual(len(task['plans']), 1)
            self.assertEqual(task['plans'][0]['trigger_time'], trigger_time)
            # 用不存在的关键字来搜索也不能报错。
            rv = client.get('/task', query_string={
                'keywords': '字节跳动',
            })
            self.assertEqual(rv.status_code, 200)
            self.assertEqual(rv.get_json()['result'], [])

    def clear_database(self):
        self.task_repository.clear()
        self.user_repository.clear()

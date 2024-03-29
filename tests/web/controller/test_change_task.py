# -*- coding: utf8 -*-
# 测试更新任务的接口
import unittest

from nest.web import main
from tests.web import helper
from tests.web.user_helper import EMAIL, PASSWORD, register_user


class ChangeTaskTestCase(unittest.TestCase):
    def setUp(self) -> None:
        location_repository = helper.location_repository
        task_repository = helper.task_repository
        user_repository = helper.user_repository
        self.task_repository = task_repository
        self.user_repository = user_repository

        self.clear_database()
        register_user(location_repository, user_repository)
        print('初始化完毕')

    def tearDown(self) -> None:
        self.clear_database()
        print('清理数据库')

    def test_change_task(self):
        with main.create_app().test_client() as client:
            client.post('/user/login', json={
                'email': EMAIL,
                'password': PASSWORD,
            })
            # 先创建一个才能修改
            rv = client.post('/task', json={
                'brief': 'Hello, nest!',
                'detail': 'first',
                'keywords': [
                    'hello',
                    'nest',
                ],
            })
            self.assertEqual(rv.status_code, 201)
            json_data = rv.get_json()
            task_id = json_data['result']['id']

            rv = client.patch('/task/{}'.format(task_id), json={
                'brief': 'Goodbye, nest!',
                'detail': 'second',
                'keywords': [
                    'goodbye',
                    'nest',
                ],
                'status': 2,
            })
            self.assertEqual(rv.status_code, 200, rv.get_data())
            json_data = rv.get_json()
            self.assertIn('result', json_data)
            task = json_data['result']
            self.assertEqual(task['brief'], 'Goodbye, nest!')
            self.assertEqual(task['detail'], 'second')
            self.assertEqual(task['id'], task_id)
            self.assertEqual(task['status'], 2)
            self.assertIn('goodbye', task['keywords'])
            self.assertIn('nest', task['keywords'])
            # 测试将关键字置空的场景
            rv = client.patch('/task/{}'.format(task_id), json={
                'keywords': [],
            })
            self.assertEqual(rv.status_code, 200)
            json_data = rv.get_json()
            self.assertIn('result', json_data)
            task = json_data['result']
            self.assertEqual(task['keywords'], [])

    def clear_database(self):
        self.task_repository.clear()
        self.user_repository.clear()

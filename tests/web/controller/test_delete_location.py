# -*- coding: utf8 -*-
import unittest

from nest.repository.location import DatabaseLocationRepository
from nest.repository.plan import DatabasePlanRepository
from nest.repository.task import DatabaseTaskRepository
from nest.repository.user import DatabaseUserRepository
from nest.web import main
from tests.web.user_helper import EMAIL, PASSWORD, register_user
from tests.web.helper import mysql_connection


class DeleteLocationTestCase(unittest.TestCase):
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

    def test_delete_location(self):
        with main.create_app().test_client() as client:
            client.post('/user/login', json={
                'email': EMAIL,
                'password': PASSWORD,
            })
            # 创建一个新地点
            rv = client.post('/location', json={
                'name': '测试用的地点',
            })
            self.assertEqual(rv.status_code, 201)
            json_data = rv.get_json()
            location_id = json_data['result']['id']
            # 创建任务以便联表查询
            rv = client.post('/task', json={
                'brief': 'test',
            })
            self.assertEqual(rv.status_code, 201)
            json_data = rv.get_json()
            task_id = json_data['result']['id']

            rv = client.post('/plan', json={
                'location_id': location_id,
                'repeat_type': 'hourly',
                'task_id': task_id,
                'trigger_time': '2021-02-20 17:39:00',
            })
            self.assertEqual(rv.status_code, 201)
            json_data = rv.get_json()
            self.assertIsInstance(json_data['result']['id'], int)

            # 先测试由于地点被使用，删除失败的情况。
            rv = client.delete('/location/{}'.format(location_id))
            print('rv.get_data()', rv.get_data())
            self.assertEqual(rv.status_code, 422)
            # 再测试删除了计划后，可以删除地点的情况。
            rv = client.delete('/plan/{}'.format(json_data['result']['id']))
            self.assertEqual(rv.get_json()['status'], 'success')

            rv = client.delete('/location/{}'.format(location_id))
            self.assertEqual(rv.status_code, 200)

    def clear_database(self):
        self.plan_repository.clear()
        self.task_repository.clear()
        self.user_repository.clear()

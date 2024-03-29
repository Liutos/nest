# -*- coding: utf8 -*-
# 测试更新地点的接口
import base64
import unittest

from nest.web import main
from tests.web.user_helper import EMAIL, PASSWORD, register_user
from tests.web.helper import (
    location_repository,
    user_repository,
)


class ChangeLocationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.location_repository = location_repository
        self.user_repository = user_repository

        self.clear_database()
        register_user(location_repository, user_repository)

    def tearDown(self) -> None:
        self.clear_database()

    def test_change_location(self):
        with main.create_app().test_client() as client:
            client.post('/user/login', json={
                'email': EMAIL,
                'password': PASSWORD,
            })
            # 先创建一个才能修改
            rv = client.post('/location', json={
                'name': '家里',
            })
            self.assertEqual(rv.status_code, 201)
            json_data = rv.get_json()
            location_id = json_data['result']['id']

            rv = client.patch('/location/{}'.format(location_id), json={
                'name': '公司',
            })
            self.assertEqual(rv.status_code, 200)
            print('rv.get_data()', rv.get_data())
            json_data = rv.get_json()
            self.assertIn('result', json_data)
            location = json_data['result']
            self.assertEqual(location['name'], '公司')
            self.assertEqual(location['id'], location_id)

    def test_create_location_with_basic_auth(self):
        """测试使用 HTTP Basic Auth 代替登录操作的场景。"""
        with main.create_app().test_client() as client:
            # 先创建一个才能修改
            rv = client.post('/location', headers={
                'Authorization': 'Basic ' + base64.b64encode((EMAIL + ':' + PASSWORD).encode('UTF-8')).decode('ASCII'),
            }, json={
                'name': '家里',
            })
            print('rv.get_json()', rv.get_json())
            self.assertEqual(rv.status_code, 201)

    def clear_database(self):
        self.location_repository.clear()
        self.user_repository.clear()

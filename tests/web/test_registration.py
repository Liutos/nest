# -*- coding: utf8 -*-
# 测试注册接口
import unittest

from nest.repository.user import DatabaseUserRepository
from nest.web import main
from tests.web.helper import mysql_connection


class RegistrationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        DatabaseUserRepository(mysql_connection).clear()

    def tearDown(self) -> None:
        DatabaseUserRepository(mysql_connection).clear()

    def test_param_missing(self):
        with main.app.test_client() as client:
            rv = client.post('/user', json={})
            self.assertEqual(rv.status_code, 422)
            json_data = rv.get_json()
            self.assertIsInstance(json_data['error']['message'], str)

    def test_registration_succeed(self):
        with main.app.test_client() as client:
            rv = client.post('/user', json={
                'email': 'abcdefgh',
                'nickname': '昵称',
                'password': '111111',
            })
            json_data = rv.get_json()
            self.assertIn('id', json_data)
            self.assertIsInstance(json_data['id'], int)


if __name__ == '__main__':
    unittest.main(verbosity=2)

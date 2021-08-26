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
            email = 'abcdefgh'
            rv = client.post('/user', json={
                'email': email,
                'nickname': '昵称',
                'password': '111111',
            })
            json_data = rv.get_json()
            self.assertIn('id', json_data)
            self.assertIsInstance(json_data['id'], int)
            user_repository = DatabaseUserRepository(mysql_connection)
            user = user_repository.get_by_email(email)
            self.assertFalse(user.is_active())
            # 此时是无法登录的
            rv = client.post('/user/login', json={
                'email': email,
                'password': '111111',
            })
            self.assertEqual(rv.status_code, 422)

    def test_activation_succeed(self):
        """测试注册后激活用户的场景。"""
        with main.app.test_client() as client:
            email = 'abcdefgh'
            rv = client.post('/user', json={
                'email': email,
                'nickname': '昵称',
                'password': '111111',
            })
            json_data = rv.get_json()
            self.assertIn('id', json_data)
            self.assertIsInstance(json_data['id'], int)
            user_repository = DatabaseUserRepository(mysql_connection)
            user = user_repository.get_by_email(email)
            self.assertFalse(user.is_active())

            rv = client.post('/user/activation', json={
                'activate_code': user.activate_code,
                'email': email,
            })
            print('rv.get_data()', rv.get_data())
            self.assertEqual(rv.status_code, 200)
            json_data: dict = rv.get_json()
            self.assertEqual(json_data['status'], 'success')
            user = user_repository.get_by_email(email)
            self.assertTrue(user.is_active())
            # 激活后可以登录
            rv = client.post('/user/login', json={
                'email': email,
                'password': '111111',
            })
            self.assertEqual(rv.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)

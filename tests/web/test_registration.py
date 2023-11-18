# -*- coding: utf8 -*-
# 测试注册接口
from unittest.mock import patch
import unittest

from nest.service.mail import SinaMailService
from nest.web import main
from tests.web import helper


def _mock_send_activate_code(*args, email: str, **kwargs):
    print('并不会真的往{}发送邮件'.format(email))


@patch.object(SinaMailService, 'send_activate_code', _mock_send_activate_code)
class RegistrationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        helper.user_repository.clear()

    def tearDown(self) -> None:
        helper.user_repository.clear()

    def test_param_missing(self):
        with main.create_app().test_client() as client:
            rv = client.post('/user', json={})
            self.assertEqual(rv.status_code, 422)
            json_data = rv.get_json()
            self.assertIsInstance(json_data['error']['message'], str)

    def test_registration_succeed(self):
        with main.create_app().test_client() as client:
            email = 'abcdefgh'
            rv = client.post('/user', json={
                'email': email,
                'nickname': '昵称',
                'password': '111111',
            })
            json_data = rv.get_json()
            self.assertEqual(json_data['status'], 'success')
            self.assertIn('id', json_data['result'])
            self.assertIsInstance(json_data['result']['id'], int)
            user = helper.user_repository.get_by_email(email)
            self.assertFalse(user.is_active())
            # 此时是无法登录的
            rv = client.post('/user/login', json={
                'email': email,
                'password': '111111',
            })
            self.assertEqual(rv.status_code, 422)

    def test_activation_succeed(self):
        """测试注册后激活用户的场景。"""
        with main.create_app().test_client() as client:
            email = 'abcdefgh'
            rv = client.post('/user', json={
                'email': email,
                'nickname': '昵称',
                'password': '111111',
            })
            json_data = rv.get_json()
            self.assertIn('id', json_data['result'])
            self.assertIsInstance(json_data['result']['id'], int)
            user_repository = helper.user_repository
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

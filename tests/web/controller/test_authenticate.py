# -*- coding: utf8 -*-
# 测试身份认证的功能。
import unittest

from nest.web import main
from tests.web.user_helper import register_user
from tests.web.helper import (
    location_repository,
    user_repository,
)


class AuthenticateTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.location_repository = location_repository
        self.user_repository = user_repository

        self.clear_database()
        register_user(location_repository, user_repository)

    def tearDown(self) -> None:
        self.clear_database()

    def test_authenticate_fail(self):
        """测试身份认证失败的场景。"""
        with main.create_app().test_client() as client:
            # 在没有登录的情况下访问接口。
            rv = client.post('/location', json={
                'name': '家里',
            })
            self.assertEqual(rv.status_code, 401)

    def clear_database(self):
        self.location_repository.clear()
        self.user_repository.clear()

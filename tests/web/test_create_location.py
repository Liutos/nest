# -*- coding: utf8 -*-
import unittest

from nest.web import main
from tests.web import helper
from tests.web.user_helper import register_user


class CreateLocationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """清空数据库，注册用户。"""
        self.location_repository = helper.location_repository
        self.user_repository = helper.user_repository
        self.location_repository.clear()
        self.user_repository.clear()
        register_user(self.location_repository, self.user_repository)

    def tearDown(self) -> None:
        self.location_repository.clear()
        self.user_repository.clear()

    def test_create_location(self):
        """测试创建一个地点。"""
        with main.create_app().test_client() as client:
            client.post('/user/login', json={
                'email': 'foobar.bef@gmail.com',
                'password': 'def',
            })
            name = '工地'
            rv = client.post('/location', json={
                'name': name,
            })
            json_data = rv.get_json()
            assert json_data['result']['id']
            assert json_data['result']['name'] == name

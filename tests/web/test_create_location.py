# -*- coding: utf8 -*-
import unittest

from nest.repository.location import DatabaseLocationRepository
from nest.repository.user import DatabaseUserRepository
from nest.web import main
from tests.web.helper import mysql_connection
from tests.web.user_helper import register_user


class CreateLocationTestCase(unittest.TestCase):
    def setUp(self) -> None:
        """清空数据库，注册用户。"""
        self.location_repository = DatabaseLocationRepository(
            connection=mysql_connection,
        )
        self.user_repository = DatabaseUserRepository(
            connection=mysql_connection,
        )
        self.location_repository.clear()
        self.user_repository.clear()
        register_user(self.location_repository, self.user_repository)

    def tearDown(self) -> None:
        self.location_repository.clear()
        self.user_repository.clear()

    def test_create_location(self):
        """测试创建一个地点。"""
        with main.app.test_client() as client:
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

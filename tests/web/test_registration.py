# -*- coding: utf8 -*-
# 测试注册接口
import pytest

from nest.repository.user import DatabaseUserRepository
from nest.web import main
from nest.web.db_connection import mysql_connection

_user_id = None


@pytest.fixture
def client():
    with main.app.test_client() as client:
        yield client
    # 在这里把数据库中插入的数据删掉
    if _user_id:
        user_repository = DatabaseUserRepository(mysql_connection)
        user_repository.remove(_user_id)


def test_param_missing(client):
    rv = client.post('/user', json={})
    print('type(client)', type(client))
    assert rv.status_code == 422
    json_data = rv.get_json()
    assert isinstance(json_data['message'], str)


def test_registration_succeed(client):
    rv = client.post('/user', json={
        'email': 'abcdefgh',
        'nickname': '昵称',
        'password': '111111',
    })
    json_data = rv.get_json()
    assert json_data['id']
    assert isinstance(json_data['id'], int)
    global _user_id
    _user_id = json_data['id']

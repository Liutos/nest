# -*- coding: utf8 -*-
import pytest

from nest.repository.plan import DatabasePlanRepository
from nest.web import main
from nest.web.db_connection import mysql_connection
from .user_helper import destroy_user, register_user

_plan_id = None


@pytest.fixture
def client():
    with main.app.test_client() as client:
        # 注册用户
        register_user()
        yield client
    # 在这里把数据库中插入的数据删掉
    if isinstance(_plan_id, int):
        plan_repository = DatabasePlanRepository(mysql_connection)
        plan_repository.remove(_plan_id)
    # 删除注册的用户
    destroy_user()


def test_create_plan(client):
    # 要先登录才能创建
    client.post('/user/login', json={
        'email': 'foobar.bef@gmail.com',
        'password': 'def',
    })
    rv = client.post('/plan', json={
        'task_id': 1,
        'trigger_time': '2021-02-20 17:39:00',
    })
    json_data = rv.get_json()
    print('json_data', json_data)
    assert json_data['id']
    assert isinstance(json_data['id'], int)
    global _plan_id
    _plan_id = json_data['id']

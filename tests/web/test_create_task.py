# -*- coding: utf8 -*-
# 测试创建任务接口
import pytest

from nest.repository.task import DatabaseTaskRepository
from nest.web import main
from nest.web.config import Config
from nest.web.db_connection import ConnectionPool
from .user_helper import destroy_user, register_user

_task_id = None
config = Config()
mysql_connection = ConnectionPool(config)


@pytest.fixture
def client():
    with main.app.test_client() as client:
        register_user()
        yield client
    # 在这里把数据库中插入的数据删掉
    if _task_id:
        task_repository = DatabaseTaskRepository(mysql_connection)
        task_repository.remove(_task_id)
    destroy_user()


def test_create_task(client):
    # 要先登录才能创建
    client.post('/user/login', json={
        'email': 'foobar.bef@gmail.com',
        'password': 'def',
    })
    rv = client.post('/task', json={
        'brief': 'Hello, nest!',
    })
    print('rv', rv)
    json_data = rv.get_json()
    assert json_data['id']
    assert isinstance(json_data['id'], int)
    global _task_id
    _task_id = json_data['id']

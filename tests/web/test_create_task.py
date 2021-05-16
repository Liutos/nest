# -*- coding: utf8 -*-
# 测试创建任务接口
import pytest

from nest.repository.location import DatabaseLocationRepository
from nest.repository.task import DatabaseTaskRepository
from nest.repository.user import DatabaseUserRepository
from nest.web import main
from .user_helper import register_user
from tests.web.helper import mysql_connection

_task_id = None
location_repository = DatabaseLocationRepository(
    connection=mysql_connection,
)
task_repository = DatabaseTaskRepository(
    connection=mysql_connection,
)
user_repository = DatabaseUserRepository(
    connection=mysql_connection,
)


def clear_database():
    task_repository.clear()
    user_repository.clear()


# 写法来自这里：https://docs.pytest.org/en/stable/xunit_setup.html
def setup_module():
    clear_database()
    register_user(location_repository, user_repository)
    print('初始化完毕')


def teardown_module():
    clear_database()
    print('清理数据库')


@pytest.fixture
def client():
    with main.app.test_client() as client:
        client.post('/user/login', json={
            'email': 'foobar.bef@gmail.com',
            'password': 'def',
        })
        yield client


def test_create_task(client):
    rv = client.post('/task', json={
        'brief': 'Hello, nest!',
    })
    print('rv', rv)
    json_data = rv.get_json()
    assert json_data['result']['id']
    assert isinstance(json_data['result']['id'], int)
    global _task_id
    _task_id = json_data['result']['id']

# -*- coding: utf8 -*-
# 测试创建任务接口
import pytest

from nest.repository.location import DatabaseLocationRepository
from nest.repository.task import DatabaseTaskRepository
from nest.repository.user import DatabaseUserRepository
from nest.web import main
from .user_helper import register_user
from tests.web.helper import mysql_connection

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


def test_change_task(client):
    # 先创建一个才能修改
    rv = client.post('/task', json={
        'brief': 'Hello, nest!',
        'keywords': [
            'hello',
            'nest',
        ],
    })
    json_data = rv.get_json()
    _task_id = json_data['result']['id']
    rv = client.patch('/task/{}'.format(_task_id), json={
        'brief': 'Goodbye, nest!',
        'keywords': [
            'goodbye',
            'nest',
        ],
        'status': 2,
    })
    json_data = rv.get_json()
    assert 'result' in json_data
    task = json_data['result']
    assert task['brief'] == 'Goodbye, nest!'
    assert task['id'] == _task_id
    assert task['status'] == 2
    assert 'goodbye' in task['keywords']
    assert 'nest' in task['keywords']

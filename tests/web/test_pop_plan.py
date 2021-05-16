# -*- coding: utf8 -*-
from datetime import datetime
import pytest
import time

from nest.repository.location import DatabaseLocationRepository
from nest.repository.plan import DatabasePlanRepository
from nest.repository.task import DatabaseTaskRepository
from nest.repository.user import DatabaseUserRepository
from nest.web import main
from .user_helper import register_user
from tests.web.helper import mysql_connection

_plan_id = None
_plan_ids = []
_task_id = None
location_repository = DatabaseLocationRepository(
    connection=mysql_connection,
)
plan_repository = DatabasePlanRepository(
    connection=mysql_connection,
)
task_repository = DatabaseTaskRepository(
    connection=mysql_connection,
)
user_repository = DatabaseUserRepository(
    connection=mysql_connection,
)


def clear_database():
    plan_repository.clear()
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
    # 创建任务以便联表查询
    rv = client.post('/task', json={
        'brief': 'test',
    })
    json_data = rv.get_json()
    assert json_data['result']['id']
    global _task_id
    _task_id = json_data['result']['id']


def test_create_plan(client):
    """创建一个提醒"""
    now = datetime.now()
    time.sleep(1)
    rv = client.post('/plan', json={
        'repeat_type': 'hourly',
        'task_id': _task_id,
        'trigger_time': now.strftime('%Y-%m-%d %H:%M:%S'),
    })
    json_data = rv.get_json()
    assert json_data['status'] == 'success'
    assert json_data['result']['id']
    assert isinstance(json_data['result']['id'], int)
    global _plan_id
    _plan_id = json_data['result']['id']


def test_pop_plan(client):
    """测试弹出计划的功能。"""
    rv = client.post('/plan/pop', json={
        'size': 1,
    })
    json_data = rv.get_json()
    print('json_data', json_data)
    assert json_data['status'] == 'success'
    plans = json_data['result']
    assert isinstance(plans, list)
    assert len(plans) == 1
    plan = plans[0]
    assert plan['id'] == _plan_id

# -*- coding: utf8 -*-
import pytest

from nest.web import main
from . import helper
from .user_helper import register_user

_plan_ids = []
_task_id = None
location_repository = helper.location_repository
plan_repository = helper.plan_repository
task_repository = helper.task_repository
user_repository = helper.user_repository


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
    with main.create_app().test_client() as client:
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
    global _task_id
    _task_id = json_data['result']['id']


def test_create_plan(client):
    rv = client.post('/plan', json={
        'repeat_type': 'hourly',
        'task_id': _task_id,
        'trigger_time': '2021-02-20 17:39:00',
    })
    json_data = rv.get_json()
    assert json_data['result']['id']
    assert isinstance(json_data['result']['id'], int)
    global _plan_ids
    _plan_ids.append(json_data['result']['id'])


def test_delete_plan(client):
    rv = client.delete('/plan/{}'.format(_plan_ids[0]))
    assert rv.get_json()['status'] == 'success'
    # 检查一下确实不在了
    plan = plan_repository.find_by_id(_plan_ids[0])
    assert plan is None

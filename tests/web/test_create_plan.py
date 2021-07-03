# -*- coding: utf8 -*-
from datetime import timedelta
import pytest

from nest.repository.location import DatabaseLocationRepository
from nest.repository.plan import DatabasePlanRepository
from nest.repository.task import DatabaseTaskRepository
from nest.repository.user import DatabaseUserRepository
from nest.web import main
from .user_helper import register_user
from tests.web.helper import mysql_connection

_plan_ids = []
_task_id = None
# TODO: 精简一下遍布各个单元测试代码中的创建仓库的代码
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
    global _task_id
    _task_id = json_data['result']['id']


def test_create_plan(client):
    rv = client.post('/plan', json={
        'duration': 234,
        'repeat_type': 'hourly',
        'task_id': _task_id,
        'trigger_time': '2021-02-20 17:39:00',
        'visible_hours': [0, 1, 1, 2, 3, 5],
    })
    json_data = rv.get_json()
    assert json_data['result']['id']
    assert json_data['result']['duration'] == 234
    assert isinstance(json_data['result']['id'], int)
    assert isinstance(json_data['result']['visible_hours'], list)
    assert set(json_data['result']['visible_hours']) == {0, 1, 2, 3, 5}
    global _plan_ids
    _plan_ids.append(json_data['result']['id'])


def test_create_plan_again(client):
    rv = client.post('/plan', json={
        'task_id': _task_id,
        'trigger_time': '2019-02-21 17:39:00',
        'visible_wdays': [0, 2, 4, 6],
    })
    json_data = rv.get_json()
    assert json_data['result']['id']
    assert isinstance(json_data['result']['id'], int)
    assert isinstance(json_data['result']['visible_wdays'], list)
    assert set(json_data['result']['visible_wdays']) == {0, 2, 4, 6}
    global _plan_ids
    _plan_ids.append(json_data['result']['id'])


def test_list_plan(client):
    rv = client.get('/plan', query_string={
        'page': 1,
        'per_page': 10,
    })
    json_data = rv.get_json()
    plans = json_data['result']['plans']
    count = json_data['result']['count']
    assert len(plans) == 2
    assert plans[0]['id'] == _plan_ids[1]
    assert plans[1]['id'] == _plan_ids[0]
    assert plans[1]['duration'] == 234
    assert count == 2


def test_periodical_plan(client):
    """测试periodically重复模式"""
    seconds = timedelta(days=3).total_seconds()
    rv = client.post('/plan', json={
        'repeat_interval': seconds,
        'repeat_type': 'periodically',
        'task_id': _task_id,
        'trigger_time': '2021-04-24 20:34:00',
    })
    json_data = rv.get_json()
    plan = json_data['result']
    assert plan
    assert plan['repeat_interval'] == seconds

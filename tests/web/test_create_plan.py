# -*- coding: utf8 -*-
import pytest

from nest.repository.plan import DatabasePlanRepository
from nest.repository.task import DatabaseTaskRepository
from nest.web import main
from nest.infra.config import Config
from nest.infra.db_connection import ConnectionPool
from .user_helper import destroy_user, register_user
from tests.web.helper import get_config_file_path

_plan_ids = []
_task_id = None
config = Config(get_config_file_path())
mysql_connection = ConnectionPool(config)


@pytest.fixture
def client():
    with main.app.test_client() as client:
        yield client


def test_create_task(client):
    # 注册用户
    register_user()
    # 要先登录才能创建
    client.post('/user/login', json={
        'email': 'foobar.bef@gmail.com',
        'password': 'def',
    })
    # 创建任务以便联表查询
    rv = client.post('/task', json={
        'brief': 'test',
    })
    json_data = rv.get_json()
    global _task_id
    _task_id = json_data['result']['id']


def destroy_artefact():
    # 在这里把数据库中插入的数据删掉
    if len(_plan_ids) > 0:
        for plan_id in _plan_ids:
            plan_repository = DatabasePlanRepository(mysql_connection)
            plan_repository.remove(plan_id)
    DatabaseTaskRepository(mysql_connection).remove(_task_id)
    # 删除注册的用户
    destroy_user()


def test_create_plan(client):
    # 要先登录才能创建
    client.post('/user/login', json={
        'email': 'foobar.bef@gmail.com',
        'password': 'def',
    })
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
    # 要先登录才能创建
    client.post('/user/login', json={
        'email': 'foobar.bef@gmail.com',
        'password': 'def',
    })
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
    # 要先登录才能创建
    client.post('/user/login', json={
        'email': 'foobar.bef@gmail.com',
        'password': 'def',
    })
    rv = client.get('/plan', query_string={
        'page': 1,
        'per_page': 10,
    })
    json_data = rv.get_json()
    plans = json_data['result']
    assert len(plans) == 2
    assert plans[0]['id'] == _plan_ids[1]
    assert plans[1]['id'] == _plan_ids[0]
    assert plans[1]['duration'] == 234
    destroy_artefact()

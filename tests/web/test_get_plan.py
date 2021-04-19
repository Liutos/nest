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
        client.post('/user/login', json={
            'email': 'foobar.bef@gmail.com',
            'password': 'def',
        })
        yield client


def test_create_task(register_user, client):
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


def test_get_plan(client):
    rv = client.get('/plan/{}'.format(_plan_ids[0]))
    assert rv.get_json()['status'] == 'success'
    result = rv.get_json()['result']
    assert result['id'] == _plan_ids[0]
    assert result['task_id'] == _task_id
    destroy_artefact()

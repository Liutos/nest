# -*- coding: utf8 -*-
# 测试创建任务接口
import pytest

from nest.web import main
from . import helper
from .user_helper import register_user

_task_id = None
location_repository = helper.location_repository
task_repository = helper.task_repository
user_repository = helper.user_repository


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
    with main.create_app().test_client() as client:
        client.post('/user/login', json={
            'email': 'foobar.bef@gmail.com',
            'password': 'def',
        })
        yield client


def test_create_task(client):
    detail = 'This is a detailed description contains of 2\nlines.'
    rv = client.post('/task', json={
        'brief': 'Hello, nest!',
        'detail': detail,
        'keywords': [
            'hello',
            'nest',
        ],
    })
    print('rv', rv.get_data())
    json_data = rv.get_json()
    assert json_data['result']['id']
    assert isinstance(json_data['result']['id'], int)
    # 用重新查询出的结果做验证，才能证明数据都被持久化了。
    rv = client.get('/task/{}'.format(json_data['result']['id']))
    json_data = rv.get_json()
    assert json_data['result']['detail'] == detail
    assert 'hello' in json_data['result']['keywords']
    assert 'nest' in json_data['result']['keywords']
    assert json_data['result']['status'] == 1
    global _task_id
    _task_id = json_data['result']['id']

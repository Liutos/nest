# -*- coding: utf8 -*-
import os

from nest.infra.db_connection import DBUtilsConnectionPool
from nest.infra.config import Config
from nest.infra.repository import RepositoryFactory


# TODO: 需要与文件 nest/web/config.py 中的函数 _load_config 统一。
def get_config_file_path():
    current_dir = os.path.dirname(__file__)
    print('current_dir', current_dir)
    config_dir = os.path.join(current_dir, '../../nest/web/config')
    file_name = os.environ.get('MODE', 'default')
    return os.path.join(config_dir, file_name + '.ini')


config = Config(get_config_file_path())
mysql_connection = DBUtilsConnectionPool(config)
repository_factory = RepositoryFactory(mysql_connection)
# 在各个单元测试中直接使用。
location_repository = repository_factory.location()
plan_repository = repository_factory.plan()
task_repository = repository_factory.task()
user_repository = repository_factory.user()

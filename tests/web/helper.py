# -*- coding: utf8 -*-
import os

from nest.infra.db_connection import DBUtilsConnectionPool
from nest.infra.config import Config
from nest.repository.location import DatabaseLocationRepository
from nest.repository.plan import DatabasePlanRepository
from nest.repository.task import DatabaseTaskRepository
from nest.repository.user import DatabaseUserRepository


# TODO: 需要与文件 nest/web/config.py 中的函数 _load_config 统一。
def get_config_file_path():
    current_dir = os.path.dirname(__file__)
    print('current_dir', current_dir)
    config_dir = os.path.join(current_dir, '../../nest/web/config')
    file_name = os.environ.get('MODE', 'default')
    return os.path.join(config_dir, file_name + '.ini')


config = Config(get_config_file_path())
mysql_connection = DBUtilsConnectionPool(config)
# 在各个单元测试中直接使用。
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

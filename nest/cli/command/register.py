# -*- coding: utf8 -*-
import argparse
import os

from nest.app.use_case.registration import IParams, RegistrationUseCase
from nest.infra.config import Config
from nest.infra.db_connection import DBUtilsConnectionPool
from nest.infra.repository import RepositoryFactory


class Params(IParams):
    def __init__(self):
        parser = argparse.ArgumentParser(description='注册用户')
        parser.add_argument(
            '--email',
            dest='email',
            help='用户登录用的邮箱地址',
            required=True,
            type=str,
        )
        parser.add_argument(
            '--nickname',
            dest='nickname',
            help='用户昵称',
            required=True,
            type=str,
        )
        parser.add_argument(
            '--password',
            dest='password',
            help='用户登录时要输入的密码',
            required=True,
            type=str,
        )
        self.args = parser.parse_args()

    def get_email(self) -> str:
        return self.args.email

    def get_nickname(self):
        return self.args.nickname

    def get_password(self):
        return self.args.password


def register():
    current_dir = os.path.dirname(__file__)
    config_dir = os.path.join(current_dir, '../config')
    file_name = 'default'
    mode = os.environ.get('MODE')
    if mode == 'unittest':
        file_name = 'unittest'
    config_file = os.path.join(config_dir, file_name + '.ini')
    config = Config(config_file)
    mysql_connection = DBUtilsConnectionPool(config)
    params = Params()
    repository_factory = RepositoryFactory(mysql_connection)
    location_repository = repository_factory.location()
    user_repository = repository_factory.user()
    use_case = RegistrationUseCase(
        location_repository=location_repository,
        params=params,
        user_repository=user_repository,
    )
    use_case.run()


if __name__ == '__main__':
    register()

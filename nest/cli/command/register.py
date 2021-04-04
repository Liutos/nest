# -*- coding: utf8 -*-
import argparse

from nest.app.use_case.registration import IParams, RegistrationUseCase
# FIXME: cli不能依赖于web模块下的功能
from nest.web.db_connection import mysql_connection
from nest.web.repository import RepositoryFactory


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
    params = Params()
    user_repository = RepositoryFactory(mysql_connection).user()
    use_case = RegistrationUseCase(
        params=params,
        user_repository=user_repository,
    )
    use_case.run()


if __name__ == '__main__':
    register()

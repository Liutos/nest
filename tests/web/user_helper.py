# -*- coding: utf8 -*-
from typing import Union

from nest.repository.user import DatabaseUserRepository
from nest.app.use_case.registration import IParams, RegistrationUseCase
from nest.web.config import Config
from nest.web.db_connection import ConnectionPool
from tests.web.helper import get_config_file_path


_user_id: Union[None, int] = None
config = Config(get_config_file_path())
mysql_connection = ConnectionPool(config)


class MockParams(IParams):
    def get_email(self) -> str:
        return 'foobar.bef@gmail.com'

    def get_nickname(self):
        return 'foobaz'

    def get_password(self):
        return 'def'


def destroy_user():
    user_repository = DatabaseUserRepository(mysql_connection)
    user_repository.remove(_user_id)


def register_user():
    use_case = RegistrationUseCase(
        params=MockParams(),
        user_repository=DatabaseUserRepository(mysql_connection)
    )
    user = use_case.run()
    global _user_id
    _user_id = user.id


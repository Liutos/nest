# -*- coding: utf8 -*-
from typing import Union

from nest.app.use_case.registration import IParams, RegistrationUseCase
from nest.infra.config import Config
from nest.infra.db_connection import DBUtilsConnectionPool
from tests.web.helper import get_config_file_path


_user_id: Union[None, int] = None
config = Config(get_config_file_path())
mysql_connection = DBUtilsConnectionPool(config)


class MockParams(IParams):
    def get_email(self) -> str:
        return 'foobar.bef@gmail.com'

    def get_nickname(self):
        return 'foobaz'

    def get_password(self):
        return 'def'


def destroy_user(user_repository):
    user_repository.remove(_user_id)


def register_user(user_repository):
    use_case = RegistrationUseCase(
        params=MockParams(),
        user_repository=user_repository,
    )
    user = use_case.run()
    global _user_id
    _user_id = user.id


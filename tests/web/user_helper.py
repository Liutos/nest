# -*- coding: utf8 -*-
from typing import Union

from nest.app.entity.user import IUserRepository, UserStatus
from nest.app.use_case.registration import IParams, RegistrationUseCase
from nest.infra.config import Config
from nest.infra.db_connection import DBUtilsConnectionPool
from tests.use_case.registration.mock_mail_service import MockMailService
from tests.web.helper import get_config_file_path


EMAIL = 'foobar.bef@gmail.com'
PASSWORD = 'def'
_user_id: Union[None, int] = None
config = Config(get_config_file_path())
mysql_connection = DBUtilsConnectionPool(config)


class MockParams(IParams):
    def get_email(self) -> str:
        return EMAIL

    def get_nickname(self):
        return 'foobaz'

    def get_password(self):
        return PASSWORD


def destroy_user(user_repository):
    user_repository.remove(_user_id)


def register_user(location_repository, user_repository: IUserRepository):
    use_case = RegistrationUseCase(
        location_repository=location_repository,
        mail_service=MockMailService(),
        params=MockParams(),
        user_repository=user_repository,
    )
    user = use_case.run()
    global _user_id
    _user_id = user.id
    user.status = UserStatus.ACTIVATED
    user_repository.add(user)


# -*- coding: utf8 -*-
from nest.app.entity.user import IUserRepository, User
from nest.app.use_case.login import IAuthenticateService, PasswordError, UserNotActive


class AuthenticateService(IAuthenticateService):
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    def check_is_email_password_match(self, email: str, password: str) -> User:
        user = self._user_repository.get_by_email(email)
        if not user:
            raise PasswordError()
        if not user.is_active():
            raise UserNotActive()

        is_match = user.test_password(password)
        if not is_match:
            raise PasswordError()

        return user

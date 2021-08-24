# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.user import IUserRepository, UserStatus


class IParams(ABC):
    @abstractmethod
    def get_activate_code(self) -> str:
        pass

    @abstractmethod
    def get_email(self) -> str:
        pass


class IncorrectActivateCodeError(Exception):
    pass


class UserNotExistError(Exception):
    pass


class ActivateUserTestCase:
    def __init__(self, *, params: IParams, user_repository: IUserRepository):
        self.params = params
        self.user_repository = user_repository

    def run(self):
        email = self.params.get_email()
        user = self.user_repository.get_by_email(email)
        if user is None:
            raise UserNotExistError()

        activate_code = self.params.get_activate_code()
        if activate_code != user.activate_code:
            raise IncorrectActivateCodeError()

        user.status = UserStatus.ACTIVATED
        self.user_repository.add(user)

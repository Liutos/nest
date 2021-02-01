# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from ..entity.user import User


class EmailOccupyError(Exception):
    pass


class IParams(ABC):
    @abstractmethod
    def get_email(self) -> str:
        pass

    @abstractmethod
    def get_nickname(self):
        pass

    @abstractmethod
    def get_password(self):
        pass


class RegistrationUseCase():
    def __init__(self, *, params, user_repository):
        self.params = params
        self.user_repository = user_repository

    def run(self):
        params = self.params
        user_repository = self.user_repository
        email = params.get_email()
        if user_repository.get_by_email(email):
            raise EmailOccupyError()

        nickname = params.get_nickname()
        password = params.get_password()
        user = User.new(email, nickname, password)
        user_repository.add(user)
        return user_repository.get_by_email(email)

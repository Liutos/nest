# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from nest.app.entity.location import ILocationRepository, Location
from nest.app.entity.user import User


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


class RegistrationUseCase:
    def __init__(self, *, location_repository, params, user_repository):
        assert isinstance(location_repository, ILocationRepository)
        self.params = params
        self.location_repository = location_repository
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
        # TODO: 这里如何引入跨表的数据库事务呢？
        user_repository.add(user)
        location = Location.new(
            name='anywhere',
            user_id=user.id,
        )
        self.location_repository.add(location=location)
        return user_repository.get_by_email(email)

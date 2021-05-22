# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import Union


class Location:
    def __init__(self):
        self.id = None
        self.name = None
        self.user_id = None

    @classmethod
    def new(cls, *, id_=None, name: str, user_id: int):
        instance = Location()
        instance.id = id_
        instance.name = name
        instance.user_id = user_id
        return instance


class ILocationRepository(ABC):
    @abstractmethod
    def add(self, *, location: Location):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def find(self, *, page: int, per_page: int, user_id: int):
        pass

    @abstractmethod
    def get_default(self, *, user_id: int) -> Union[None, Location]:
        pass

# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class Location:
    def __init__(self):
        self.id = None
        self.name = None
        self.user_id = None

    @classmethod
    def new(cls, *, name: str, user_id: int):
        instance = Location()
        instance.name = name
        instance.user_id = user_id
        return instance


class ILocationRepository(ABC):
    @abstractmethod
    def add(self, *, location: Location):
        pass

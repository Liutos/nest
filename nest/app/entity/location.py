# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List, Union


class AccessDeniedError(Exception):
    """用户无权访问给定地点的错误。"""
    pass


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
    def add(self, *, location: Location):  # TODO: 重命名为save。
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def find(self, *, ids: Union[None, List[int]] = None,
             name: Union[None, str] = None, page: int, per_page: int, user_id: int):
        pass

    @abstractmethod
    def get(self, *, id_: int) -> Union[None, Location]:
        pass

    @abstractmethod
    def get_default(self, *, user_id: int) -> Union[None, Location]:
        pass

    @abstractmethod
    def remove(self, *, id_: int):
        """从存储中删除指定的地点。"""
        pass

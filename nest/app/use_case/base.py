# -*- coding: utf8 -*-
import abc

from nest.app.entity.location import ILocationRepository
from nest.app.entity.plan import IPlanRepository
from nest.app.entity.task import ITaskRepository
from nest.app.entity.user import IUserRepository


class IUnitOfWork(abc.ABC):
    @abc.abstractmethod
    def begin(self):
        """开启一个数据库事务。"""
        pass

    @abc.abstractmethod
    def commit(self):
        """提交一个数据库事务。"""
        pass

    @abc.abstractmethod
    def location(self) -> ILocationRepository:
        pass

    @abc.abstractmethod
    def plan(self) -> IPlanRepository:
        pass

    @abc.abstractmethod
    def rollback(self):
        """回滚一个数据库事务。"""
        pass

    @abc.abstractmethod
    def task(self) -> ITaskRepository:
        pass

    @abc.abstractmethod
    def user(self) -> IUserRepository:
        pass

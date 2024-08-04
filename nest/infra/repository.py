# -*- coding: utf8 -*-
from nest.app.use_case.base import IRepositoryFactory
from nest.repository.db_operation import IConnectionPool
from nest.repository.location import DatabaseLocationRepository
from nest.repository.plan import DatabasePlanRepository
from nest.repository.task import DatabaseTaskRepository
from nest.repository.user import DatabaseUserRepository


class RepositoryFactory(IRepositoryFactory):
    def __init__(self, mysql_connection):
        assert isinstance(mysql_connection, IConnectionPool)
        self._cached_connection = mysql_connection.acquire_connection()
        self.mysql_connection = mysql_connection

    def begin(self):
        self._cached_connection.begin()

    def commit(self):
        self._cached_connection.commit()

    def location(self):
        return DatabaseLocationRepository(
            connection=self._cached_connection,
        )

    def plan(self):
        return DatabasePlanRepository(self._cached_connection)

    def rollback(self):
        self._cached_connection.rollback()

    def task(self):
        return DatabaseTaskRepository(self._cached_connection)

    def user(self):
        return DatabaseUserRepository(self._cached_connection)

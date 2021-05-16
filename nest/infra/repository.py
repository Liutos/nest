# -*- coding: utf8 -*-
from nest.repository.location import DatabaseLocationRepository
from nest.repository.plan import DatabasePlanRepository
from nest.repository.task import DatabaseTaskRepository
from nest.repository.user import DatabaseUserRepository


class RepositoryFactory:
    def __init__(self, mysql_connection):
        self.mysql_connection = mysql_connection

    def location(self):
        return DatabaseLocationRepository(
            connection=self.mysql_connection
        )

    def plan(self):
        return DatabasePlanRepository(self.mysql_connection)

    def task(self):
        return DatabaseTaskRepository(self.mysql_connection)

    def user(self):
        return DatabaseUserRepository(self.mysql_connection)

# -*- coding: utf8 -*-
from ..repository.plan import DatabasePlanRepository
from ..repository.task import DatabaseTaskRepository
from ..repository.user import DatabaseUserRepository
from nest.web.db_connection import mysql_connection


class RepositoryFactory:
    @staticmethod
    def plan():
        return DatabasePlanRepository(mysql_connection)

    @staticmethod
    def task():
        return DatabaseTaskRepository(mysql_connection)

    @staticmethod
    def user():
        return DatabaseUserRepository(mysql_connection)

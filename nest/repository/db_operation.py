# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
from typing import List


class IConnectionPool(ABC):
    @abstractmethod
    def acquire_connection(self):
        pass

    @abstractmethod
    def release_connection(self, connection):
        pass


class Connection:
    def __init__(self, connection):
        self.connection = connection

    def __getattr__(self, item):
        return getattr(self.connection, item)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('什么也不用做')


class DatabaseOperationMixin:
    def __init__(self, connection):
        assert not isinstance(connection, IConnectionPool)
        self.cached_connection = connection
        self.is_transaction = False
        self.transaction_participants: List[DatabaseOperationMixin] = []

    def commit(self):
        for repository in self.transaction_participants:
            r: DatabaseOperationMixin = repository
            r.cached_connection = None
            r.is_transaction = False

        self.cached_connection.commit()
        self.cached_connection = None
        self.is_transaction = False
        print('提交数据库事务')

    def execute_sql(self, sql: str):
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor

    def get_connection(self):
        return Connection(self.cached_connection)

    def insert_to_db(self, kvs: dict, table_name: str) -> int:
        sql = 'INSERT INTO `{}` SET'.format(table_name)
        values = []
        is_first = True
        for column_name, value in kvs.items():
            if is_first:
                separator = ' '
            else:
                separator = ', '
            sql += '{}`{}` = %s'.format(separator, column_name)
            values.append(value)
            if is_first:
                is_first = False
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, tuple(values))
                inserted_id = cursor.lastrowid
            connection.commit()
        return inserted_id

    def remove_from_db(self, id_: int, table_name: str):
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                sql = 'DELETE FROM `{}` WHERE `id` = %s'.format(table_name)
                cursor.execute(sql, (id_,))
            connection.commit()

    def rollback(self):
        for repository in self.transaction_participants:
            r: DatabaseOperationMixin = repository
            r.cached_connection = None
            r.is_transaction = False

        self.cached_connection.rollback()
        self.cached_connection = None
        self.is_transaction = False
        print('回滚数据库事务')

    def start_transaction(self, *, with_repository=None):
        self.is_transaction = True
        self.cached_connection = self.get_connection()
        if with_repository is not None:
            self.transaction_participants = with_repository
            for repository in with_repository:
                r: DatabaseOperationMixin = repository
                r.cached_connection = self.cached_connection
                r.is_transaction = True

        self.cached_connection.begin()
        print('开启数据库事务')

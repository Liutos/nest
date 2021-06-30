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
    def __init__(self, connection, pool, *, is_transaction=False):
        assert isinstance(pool, IConnectionPool)
        self.connection = connection
        self.is_transaction = is_transaction
        self.pool = pool

    def __getattr__(self, item):
        return getattr(self.connection, item)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: 这里让连接自己归还给连接池好像不是一个好主意？
        if not self.is_transaction:
            self.pool.release_connection(self.connection)


class DatabaseOperationMixin:
    def __init__(self, pool):
        assert isinstance(pool, IConnectionPool)
        self.cached_connection = None
        self.is_transaction = False
        self.pool = pool
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
        if self.cached_connection:
            return self.cached_connection

        connection = self.pool.acquire_connection()
        return Connection(connection, self.pool, is_transaction=self.is_transaction)

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

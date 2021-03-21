# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class IConnectionPool(ABC):
    @abstractmethod
    def acquire_connection(self):
        pass

    @abstractmethod
    def release_connection(self, connection):
        pass


class Connection:
    def __init__(self, connection, pool):
        assert isinstance(pool, IConnectionPool)
        self.connection = connection
        self.pool = pool

    def __getattr__(self, item):
        return getattr(self.connection, item)

    def __enter__(self):
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.release_connection(self.connection)


class DatabaseOperationMixin:
    def __init__(self, pool):
        assert isinstance(pool, IConnectionPool)
        self.pool = pool

    def get_connection(self):
        connection = self.pool.acquire_connection()
        return Connection(connection, self.pool)

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

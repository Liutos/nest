# -*- coding: utf8 -*-
from dbutils.pooled_db import PooledDB
import pymysql.cursors
from pymysqlpool.pool import Pool

from nest.repository.db_operation import IConnectionPool


class ConnectionPool(IConnectionPool):
    def __init__(self, config):
        mysql_section = config['mysql']
        database = mysql_section['database']
        host = mysql_section['host']
        password = mysql_section['password']
        user = mysql_section['user']
        _pool = Pool(
            cursorclass=pymysql.cursors.DictCursor,
            database=database,
            host=host,
            password=password,
            user=user,
        )
        _pool.init()
        self._pool = _pool

    def acquire_connection(self):
        connection = self._pool.get_conn()
        connection.ping(reconnect=True)
        return connection

    def release_connection(self, connection):
        self._pool.release(connection)


class DBUtilsConnectionPool(IConnectionPool):
    def __init__(self, config):
        mysql_section = config['mysql']
        database = mysql_section['database']
        host = mysql_section['host']
        password = mysql_section['password']
        user = mysql_section['user']
        self.pool = PooledDB(
            autocommit=True,
            creator=pymysql,
            cursorclass=pymysql.cursors.DictCursor,
            database=database,
            host=host,
            password=password,
            user=user,
        )

    def acquire_connection(self):
        return self.pool.connection()

    def release_connection(self, connection):
        return connection.close()

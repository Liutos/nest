# -*- coding: utf8 -*-
import pymysql.cursors
from pymysqlpool.pool import Pool

from nest.repository.db_operation import IConnectionPool
from nest.web.config import config

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


class ConnectionPool(IConnectionPool):
    def acquire_connection(self):
        connection = _pool.get_conn()
        connection.ping(reconnect=True)
        return connection

    def release_connection(self, connection):
        _pool.release(connection)


mysql_connection = ConnectionPool()

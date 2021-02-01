# -*- coding: utf8 -*-
import pymysql.cursors

from nest.web.config import config

mysql_section = config['mysql']
database = mysql_section['database']
host = mysql_section['host']
password = mysql_section['password']
user = mysql_section['user']
mysql_connection = pymysql.connect(
    cursorclass=pymysql.cursors.DictCursor,
    database=database,
    host=host,
    password=password,
    user=user,
)

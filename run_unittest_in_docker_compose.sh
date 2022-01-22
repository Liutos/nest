#!/bin/bash
# 在 docker-compose 所启动的 web 容器中执行单元测试。
set -e
# 先创建数据库，再创建表，用于单元测试。
mysql --host mysql --port 3306 -u root -proot -e 'DROP DATABASE IF EXISTS nest_unittest'
mysql --host mysql --port 3306 -u root -proot -e 'CREATE DATABASE nest_unittest CHARACTER SET utf8mb4'
mysql --host mysql --port 3306 -u root -proot nest_unittest < ./nest/repository/DDL/init_nest.sql
# 真正执行单元测试。
MODE=unittest pytest -ra -s -x ./
# -*- coding: utf8 -*-
import unittest

from nest.app.entity.task import Task
from nest.app.entity.user import User
from nest.infra.repository import MysqlUnitOfWork
from tests.web.helper import mysql_connection


class DeleteTaskUseCase(unittest.TestCase):
    def setUp(self) -> None:
        """创建用户和任务。"""
        factory = MysqlUnitOfWork(mysql_connection)
        self.user_repository = factory.user()
        self.task_repository = factory.task()

        self._clear_tables()
        email = 'foobar.bef@gmail.com'
        nickname = 'foobaz'
        password = 'def'
        user = User.new(email, nickname, password)
        self.user_repository.add(user)
        task = Task.new('Hello, world!', user.id, keywords=['hello', 'world'])
        self.task = task
        self.task_repository.add(task)

    def tearDown(self) -> None:
        self._clear_tables()

    def test_delete_task(self):
        """删除任务及其关键字。"""
        self.task_repository.remove(self.task.id)
        cursor = self.task_repository.execute_sql('SELECT COUNT(0) FROM `t_task_keyword`')
        row = cursor.fetchone()
        self.assertEqual(row['COUNT(0)'], 0)

    def _clear_tables(self):
        self.user_repository.execute_sql('DELETE FROM `t_user`')
        self.task_repository.execute_sql('DELETE FROM `t_task`')
        self.task_repository.execute_sql('DELETE FROM `t_task_keyword`')
        self.task_repository.execute_sql('DELETE FROM `t_keyword`')


if __name__ == '__main__':
    unittest.main(verbosity=2)

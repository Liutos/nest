# -*- coding: utf8 -*-
from datetime import datetime
from typing import Union

from nest.app.entity.task import ITaskRepository, Task
from nest.repository.db_operation import DatabaseOperationMixin


class DatabaseTaskRepository(DatabaseOperationMixin, ITaskRepository):
    def __init__(self, connection):
        super(DatabaseTaskRepository, self).__init__(connection)

    def add(self, task: Task):
        now = datetime.now()
        insert_id = self.insert_to_db({
            'brief': task.brief,
            'user_id': task.user_id,
            'ctime': now,
            'mtime': now,
        }, 't_task')

        task.id = insert_id

    def find(self, *, count, start, user_id) -> [Task]:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `t_task` WHERE `user_id` = %s ORDER BY `ctime` DESC LIMIT %s OFFSET %s"
                cursor.execute(sql, (user_id, count, start))
                return cursor.fetchall()

    def find_by_id(self, id_: int) -> Union[None, Task]:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `t_task` WHERE `id` = %s"
                cursor.execute(sql, (id_,))
                row = cursor.fetchone()
                if row is None:
                    return None

                task = Task()
                task.brief = row['brief']
                task.id = row['id']
                task.user_id = row['user_id']
                return task

    def remove(self, task: Union[Task, int]):
        if isinstance(task, Task):
            task_id = task.id
        else:
            assert isinstance(task, int)
            task_id = task

        self.remove_from_db(task_id, 't_task')

# -*- coding: utf8 -*-
from datetime import datetime
from typing import List, Union

from pypika import Order, Query, Table

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

    def clear(self):
        """
        清空整个t_task表，用于单元测试的初始化。
        """
        plan_table = Table('t_task')
        query = Query\
            .from_(plan_table)\
            .delete()
        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

    def find(self, *, count, start, user_id,
             task_ids: Union[None, List[int]] = None) -> [Task]:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                task_table = Table('t_task')
                query = Query\
                    .from_(task_table)\
                    .select(task_table.star)\
                    .where(task_table.user_id == user_id)\
                    .orderby(task_table.ctime, order=Order.desc)\
                    .limit(count)\
                    .offset(start)
                if task_ids is not None:
                    query = query.where(task_table.id.isin(task_ids))

                sql = query.get_sql(quote_char=None)
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [self._row_to_task(row) for row in rows]

    def find_by_id(self, id_: int) -> Union[None, Task]:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `t_task` WHERE `id` = %s"
                cursor.execute(sql, (id_,))
                row = cursor.fetchone()
                if row is None:
                    return None

                return self._row_to_task(row)

    def remove(self, task: Union[Task, int]):
        if isinstance(task, Task):
            task_id = task.id
        else:
            assert isinstance(task, int)
            task_id = task

        self.remove_from_db(task_id, 't_task')

    def _row_to_task(self, row):
        task = Task()
        task.brief = row['brief']
        task.id = row['id']
        task.user_id = row['user_id']
        return task

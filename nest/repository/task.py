# -*- coding: utf8 -*-
from datetime import datetime
from typing import List, Optional, Union

from pypika import Order, Query, Table, Tables

from nest.app.entity.task import ITaskRepository, Task, TaskStatus
from nest.repository.db_operation import DatabaseOperationMixin


class DatabaseTaskRepository(DatabaseOperationMixin, ITaskRepository):
    def __init__(self, connection):
        super(DatabaseTaskRepository, self).__init__(connection)

    def add(self, task: Task):
        if task.id is None:
            # 依次插入t_keyword、t_task，以及t_task_keyword表。
            keywords = task.keywords
            keyword_ids = [self._ensure_keyword_exist(keyword) for keyword in keywords]
            now = datetime.now()
            insert_id = self.insert_to_db({
                'brief': task.brief,
                'status': task.status and task.status.value,
                'user_id': task.user_id,
                'ctime': now,
                'mtime': now,
            }, 't_task')
            for keyword_id in keyword_ids:
                self.insert_to_db({
                    'keyword_id': keyword_id,
                    'task_id': insert_id,
                }, 't_task_keyword')

            task.id = insert_id
        else:
            # t_keyword表只增不减，先更新t_task表，再删除t_task_keyword表不再存在的记录。
            task_table, task_keyword_table = Tables('t_task', 't_task_keyword')
            query = Query\
                .update(task_table)\
                .set(task_table.brief, task.brief)\
                .where(task_table.id == task.id)
            if task.status:
                query = query.set(task_table.status, task.status.value)
            sql = query.get_sql(quote_char=None)
            self.execute_sql(sql)

            sql = Query\
                .from_(task_keyword_table)\
                .where(task_keyword_table.task_id == task.id)\
                .delete()\
                .get_sql(quote_char=None)
            self.execute_sql(sql)

            query = Query\
                .into(task_keyword_table)\
                .columns('keyword_id', 'task_id')
            for keyword in task.keywords:
                keyword_id = self._ensure_keyword_exist(keyword)
                query = query.insert(keyword_id, task.id)
            sql = query.get_sql(quote_char=None)
            print('sql', sql)
            self.execute_sql(sql)

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

    def find(self, *, count, keyword: Optional[str] = None,
             start, user_id,
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
                if keyword is not None:
                    keyword_id = self._find_keyword(keyword)
                    task_keyword_table = Table('t_task_keyword')
                    subquery = Query\
                        .from_(task_keyword_table)\
                        .select(task_keyword_table.task_id)\
                        .where(task_keyword_table.keyword_id == keyword_id)
                    query = query.where(task_table.id.isin(subquery))
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

    def remove(self, id_: int):
        self.remove_from_db(id_, 't_task')

    def _ensure_keyword_exist(self, keyword: str) -> int:
        """找出关键字的ID，或写入该关键字。"""
        keyword_id = self._find_keyword(keyword)
        if keyword_id is not None:
            return keyword_id
        return self.insert_to_db({
            'content': keyword,
        }, 't_keyword')

    def _find_keyword(self, keyword: str) -> Optional[int]:
        keyword_table = Table('t_keyword')
        query = Query \
            .from_(keyword_table) \
            .select(keyword_table.star) \
            .where(keyword_table.content == keyword)
        sql = query.get_sql(quote_char=None)
        cursor = self.execute_sql(sql)
        row = cursor.fetchone()
        return row and row.get('id')

    def _row_to_task(self, row):
        task = Task()
        task.brief = row['brief']
        task.id = row['id']
        task.status = row['status'] and TaskStatus(row['status'])
        task.user_id = row['user_id']
        # 取出任务的所有关键字
        keyword_table, task_keyword_table = Tables('t_keyword', 't_task_keyword')
        subquery = Query\
            .from_(task_keyword_table)\
            .select(task_keyword_table.keyword_id)\
            .where(task_keyword_table.task_id == row['id'])
        query = Query\
            .from_(keyword_table)\
            .select(keyword_table.star)\
            .where(keyword_table.id.isin(subquery))
        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                task.keywords = [row['content'] for row in rows]
        return task

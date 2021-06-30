# -*- coding: utf8 -*-
from datetime import datetime, timedelta
import json
from typing import List, Union

from pypika import Order, Query, Table, Tables

from nest.app.entity.plan import IPlanRepository, Plan
from nest.repository.db_operation import DatabaseOperationMixin


class DatabasePlanRepository(DatabaseOperationMixin, IPlanRepository):
    def __init__(self, connection):
        super(DatabasePlanRepository, self).__init__(connection)

    def add(self, plan: Plan):
        """
        将计划存储到数据库，或更新数据库已有的计划。
        """
        # TODO: 统一一下插入和更新时两种不同风格的写法。这里统一为用pypika、而不是自己发明一种写法会更好。
        if plan.id is None:
            now = datetime.now()
            repeat_interval: Union[None, timedelta, int] = plan.repeat_interval
            if repeat_interval is not None:
                repeat_interval = int(repeat_interval.total_seconds())

            insert_id = self.insert_to_db({
                'duration': plan.duration,
                'location_id': plan.location_id,
                'repeat_interval': repeat_interval,
                'repeat_type': plan.repeat_type,
                'task_id': plan.task_id,
                'trigger_time': plan.trigger_time,
                'visible_hours': json.dumps(list(plan.visible_hours)),
                'visible_wdays': json.dumps(list(plan.visible_wdays)),
                'ctime': now,
                'mtime': now,
            }, 't_plan')

            plan.id = insert_id
        else:
            plan_table = Table('t_plan')
            repeat_interval: Union[None, timedelta] = plan.repeat_interval
            if repeat_interval is not None:
                repeat_interval = int(repeat_interval.total_seconds())

            query = Query\
                .update(plan_table)\
                .set(plan_table.duration, plan.duration)\
                .set(plan_table.location_id, plan.location_id)\
                .set(plan_table.repeat_interval, repeat_interval)\
                .set(plan_table.repeat_type, plan.repeat_type)\
                .set(plan_table.trigger_time, plan.trigger_time)\
                .set(plan_table.visible_hours, json.dumps(plan.visible_hours)) \
                .set(plan_table.visible_wdays, json.dumps(plan.visible_wdays))\
                .where(plan_table.id == plan.id)
            sql = query.get_sql(quote_char=None)
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql)

    def clear(self):
        """
        清空整个t_plan表，用于单元测试的初始化。
        """
        plan_table = Table('t_plan')
        query = Query\
            .from_(plan_table)\
            .delete()
        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

    def find_as_queue(self, *, location_ids: Union[None, List[int]] = None,
                      max_trigger_time=None,
                      page: int, per_page: int, user_id: int) -> List[Plan]:
        plan_table, task_table = Tables('t_plan', 't_task')
        query = Query\
            .from_(plan_table)\
            .left_join(task_table)\
            .on(plan_table.task_id == task_table.id)\
            .select(plan_table.star)\
            .where(task_table.user_id == user_id)\
            .orderby(plan_table.trigger_time, order=Order.asc)\
            .limit(per_page)\
            .offset((page - 1) * per_page)

        if location_ids:
            query = query.where(plan_table.location_id.isin(location_ids))

        if isinstance(max_trigger_time, datetime):
            query = query.where(plan_table.trigger_time < max_trigger_time)

        print('sql', query.get_sql(quote_char=None))
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query.get_sql(quote_char=None))
                plan_dicts = cursor.fetchall()

        return [self._row2entity(row) for row in plan_dicts]

    def find_by_id(self, id_: int) -> Union[None, Plan]:
        plan_table = Table('t_plan')
        query = Query\
            .from_(plan_table)\
            .select(plan_table.star)\
            .where(plan_table.id == id_)
        sql = query.get_sql(quote_char=None)
        print('sql', sql)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                plan_dict = cursor.fetchone()
                if plan_dict is None:
                    return None
                return self._row2entity(plan_dict)

    def find_by_task_id(self, *, task_id: int) -> List[Plan]:
        plan_table = Table('t_plan')
        query = Query \
            .from_(plan_table) \
            .select(plan_table.star) \
            .where(plan_table.task_id == task_id)
        sql = query.get_sql(quote_char=None)
        cursor = self.execute_sql(sql)
        rows = cursor.fetchall()
        return list(map(self._row2entity, rows))

    def remove(self, id_: int):
        self.remove_from_db(id_, 't_plan')

    def _row2entity(self, row: dict):
        plan = Plan()
        plan.duration = row['duration']
        plan.id = row['id']
        plan.location_id = row['location_id']
        if isinstance(row['repeat_interval'], int):
            plan.repeat_interval = timedelta(seconds=row['repeat_interval'])
        plan.repeat_type = row['repeat_type']
        plan.task_id = row['task_id']
        plan.trigger_time = row['trigger_time']
        plan.visible_hours = json.loads(row.get('visible_hours') or '[]')
        plan.visible_wdays = json.loads(row.get('visible_wdays') or '[]')
        return plan

# -*- coding: utf8 -*-
from datetime import datetime
import json
from typing import List

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
        if plan.id is None:
            now = datetime.now()
            insert_id = self.insert_to_db({
                'duration': plan.duration,
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
            query = Query\
                .update(plan_table)\
                .set(plan_table.duration, plan.duration)\
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

    def find_as_queue(self, *, page: int, per_page: int, user_id: int, max_trigger_time=None) -> List[Plan]:
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

        if isinstance(max_trigger_time, datetime):
            query = query.where(plan_table.trigger_time < max_trigger_time)

        print('sql', query.get_sql(quote_char=None))
        plans = []
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query.get_sql(quote_char=None))
                plan_dicts = cursor.fetchall()

        # TODO: 这里的代码需要与find_by_id中的统一起来。
        for plan_dict in plan_dicts:
            plan = Plan()
            plan.duration = plan_dict['duration']
            plan.id = plan_dict['id']
            plan.repeat_type = plan_dict['repeat_type']
            plan.task_id = plan_dict['task_id']
            plan.trigger_time = plan_dict['trigger_time']
            plan.visible_hours = json.loads(plan_dict.get('visible_hours') or '[]')
            plan.visible_wdays = json.loads(plan_dict.get('visible_wdays') or '[]')
            plans.append(plan)
        return plans

    def find_by_id(self, id_: int) -> Plan:
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
                plan = Plan()
                plan.duration = plan_dict['duration']
                plan.id = plan_dict['id']
                plan.repeat_type = plan_dict['repeat_type']
                plan.task_id = plan_dict['task_id']
                plan.trigger_time = plan_dict['trigger_time']
                plan.visible_hours = json.loads(plan_dict.get('visible_hours') or '[]')
                plan.visible_wdays = json.loads(plan_dict.get('visible_wdays') or '[]')
                return plan

    def remove(self, id_: int):
        self.remove_from_db(id_, 't_plan')

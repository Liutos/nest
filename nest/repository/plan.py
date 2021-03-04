# -*- coding: utf8 -*-
from datetime import datetime
from typing import List

from nest.app.entity.plan import IPlanRepository, Plan
from nest.repository.db_operation import DatabaseOperationMixin


class DatabasePlanRepository(DatabaseOperationMixin, IPlanRepository):
    def __init__(self, connection):
        super(DatabasePlanRepository, self).__init__(connection)

    def add(self, plan: Plan):
        now = datetime.now()
        insert_id = self.insert_to_db({
            'task_id': plan.task_id,
            'trigger_time': plan.trigger_time,
            'ctime': now,
            'mtime': now,
        }, 't_plan')

        plan.id = insert_id

    def find_as_queue(self, *, page: int, per_page: int, user_id: int, max_trigger_time=None) -> List[Plan]:
        conditions = [
            '`t_task`.`user_id` = %s',
        ]
        values = [
            user_id,
        ]
        if isinstance(max_trigger_time, datetime):
            conditions.append('`t_plan`.`trigger_time` < %s')
            values.append(max_trigger_time)

        select_part = 'SELECT * FROM `t_plan` LEFT JOIN `t_task` ON `t_plan`.`task_id` = `t_task`.`id`'
        where_part = ' WHERE ' + ' AND '.join(conditions)
        order_part = ' ORDER BY `t_plan`.`trigger_time` ASC LIMIT %s OFFSET %s'
        sql = select_part + where_part + order_part
        print('sql', sql)
        values.append(per_page)
        values.append((page - 1) * per_page)
        print('values', values)
        plans = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql, tuple(values))
            plan_dicts = cursor.fetchall()

        for plan_dict in plan_dicts:
            plan = Plan()
            plan.id = plan_dict['id']
            plan.task_id = plan_dict['task_id']
            plan.trigger_time = plan_dict['trigger_time']
            plans.append(plan)
        return plans

    def remove(self, id_: int):
        self.remove_from_db(id_, 't_plan')

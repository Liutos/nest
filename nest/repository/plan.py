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

    def find_as_queue(self, *, page: int, per_page: int, user_id: int) -> List[Plan]:
        with self.connection.cursor() as cursor:
            limit = per_page
            offset = (page - 1) * per_page
            sql = 'SELECT * FROM `t_plan` LEFT JOIN `t_task` ON `t_plan`.`task_id` = `t_task`.`id` WHERE `t_task`.`user_id` = %s ORDER BY `t_plan`.`trigger_time` ASC LIMIT %s OFFSET %s'
            cursor.execute(sql, (user_id, limit, offset))
            return cursor.fetchall()

    def remove(self, id_: int):
        self.remove_from_db(id_, 't_plan')

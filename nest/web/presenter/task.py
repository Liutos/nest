# -*- coding: utf8 -*-
from nest.app.entity.task import Task


class Presenter:
    def __init__(self, *, task: Task):
        self.task = task

    def build(self):
        return {
                'brief': self.task.brief,
                'id': self.task.id,
                'keywords': self.task.keywords,
                'status': self.task.status.value,
        }

# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from ..entity.certificate import ICertificateRepository
from ..entity.task import ITaskRepository, Task


class IParams(ABC):
    @abstractmethod
    def get_brief(self) -> str:
        pass

    @abstractmethod
    def get_certificate_id(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class CreateTaskUseCase:
    def __init__(self, *, authentication_plugin, certificate_repository,
                 params, task_repository):
        assert isinstance(certificate_repository, ICertificateRepository)
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.authentication_plugin = authentication_plugin
        self.certificate_repository = certificate_repository
        self.params = params
        self.task_repository = task_repository

    def run(self):
        self.authentication_plugin.authenticate()
        # 从这里开始才是正式的创建任务的逻辑
        params = self.params
        brief = params.get_brief()
        user_id = params.get_user_id()
        task = Task.new(brief, user_id)
        task_repository = self.task_repository
        task_repository.add(task)
        return task

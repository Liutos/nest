# -*- coding: utf8 -*-
from abc import ABC, abstractmethod

from ..entity.certificate import ICertificateRepository
from ..entity.task import ITaskRepository
from .authentication_plugin import IAuthenticationPlugin


class IParams(ABC):
    @abstractmethod
    def get_certificate_id(self) -> int:
        pass

    @abstractmethod
    def get_task_id(self) -> int:
        pass

    @abstractmethod
    def get_user_id(self) -> int:
        pass


class GetTaskUseCase:
    def __init__(self, *, authentication_plugin, certificate_repository, params, task_repository):
        assert isinstance(authentication_plugin, IAuthenticationPlugin)
        assert isinstance(certificate_repository, ICertificateRepository)
        assert isinstance(params, IParams)
        assert isinstance(task_repository, ITaskRepository)
        self.authentication_plugin = authentication_plugin
        self.certificate_repository = certificate_repository
        self.params = params
        self.task_repository = task_repository

    def run(self):
        self.authentication_plugin.authenticate()
        # 以下是真正的业务逻辑
        params = self.params
        task_id = params.get_task_id()
        task_repository = self.task_repository
        task = task_repository.find_by_id(
            id_=task_id,
        )
        return task

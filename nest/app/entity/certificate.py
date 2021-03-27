# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class Certificate:
    def __init__(self):
        self.id = None
        self.user_id = None

    @classmethod
    def new(cls, user_id):
        instance = Certificate()
        instance.user_id = user_id
        return instance


class ICertificateRepository(ABC):
    @abstractmethod
    def add(self, certificate: Certificate):
        pass

    @abstractmethod
    def get_by_certificate_id(self, certificate_id: str) -> Certificate:
        pass

# -*- coding: utf8 -*-
from abc import ABC, abstractmethod


class IAuthenticationPlugin(ABC):
    @abstractmethod
    def authenticate(self):
        pass


class InvalidCertificateError(Exception):
    pass


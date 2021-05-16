# -*- coding: utf8 -*-
from abc import ABC, abstractmethod
import hashlib
import random
import string
from typing import List


class User:
    def __init__(self):
        self.email = None
        self.id = None
        self.nickname = None
        self.password_hash = None
        self.salt = None

    @classmethod
    def new(cls, email, nickname, password):
        instance = User()
        instance.email = email
        instance.nickname = nickname
        salt = instance._make_salt()
        instance.password_hash = instance._hash_password(password, salt)
        instance.salt = salt
        return instance

    def test_password(self, password):
        """
        Return true or false depends on whether password is correct.
        """
        password_hash = self._hash_password(password, self.salt)
        return password_hash == self.password_hash

    def _make_salt(self):
        """
        Generate a random salt.
        """
        # 参考这里：https://pythonexamples.org/python-generate-random-string-of-specific-length/
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=16))

    def _hash_password(self, password, salt):
        """
        Calculate the hash of password.
        """
        password_hash = hashlib.md5()
        password_hash.update((password + salt).encode('UTF-8'))
        return password_hash.hexdigest()


class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def find(self, *, page: int, per_page: int) -> List[User]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

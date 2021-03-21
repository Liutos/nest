# -*- coding: utf8 -*-
from datetime import datetime
from typing import Union

from nest.app.entity.user import IUserRepository, User
from nest.repository.db_operation import DatabaseOperationMixin


class DatabaseUserRepository(DatabaseOperationMixin, IUserRepository):
    def __init__(self, connection):
        super(DatabaseUserRepository, self).__init__(connection)

    def add(self, user: User):
        now = datetime.now()
        self.insert_to_db({
            'email': user.email,
            'nickname': user.nickname,
            'password_hash': user.password_hash,
            'salt': user.salt,
            'ctime': now,
            'mtime': now,
        }, 't_user')

        return self.get_by_email(user.email)

    def get_by_email(self, email: str) -> Union[User, None]:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `t_user` WHERE `email` = %s"
                cursor.execute(sql, (email,))
                row = cursor.fetchone()
                if row is None:
                    return None

                user = User()
                user.email = row['email']
                user.id = row['id']
                user.nickname = row['nickname']
                user.password_hash = row['password_hash']
                user.salt = row['salt']
                return user

    def remove(self, user: Union[User, int]):
        if isinstance(user, User):
            user_id = user.id
        else:
            assert isinstance(user, int)
            user_id = user

        self.remove_from_db(user_id, 't_user')

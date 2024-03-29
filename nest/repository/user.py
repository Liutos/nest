# -*- coding: utf8 -*-
from datetime import datetime
from typing import List, Union

from pypika import Query, Table

from nest.app.entity.user import IUserRepository, User, UserStatus
from nest.repository.db_operation import DatabaseOperationMixin


class DatabaseUserRepository(DatabaseOperationMixin, IUserRepository):
    def __init__(self, connection):
        super(DatabaseUserRepository, self).__init__(connection)

    def add(self, user: User):
        now = datetime.now()
        if user.id is None:
            id_ = self.insert_to_db({
                'activate_code': user.activate_code,
                'email': user.email,
                'nickname': user.nickname,
                'password_hash': user.password_hash,
                'salt': user.salt,
                'status': user.status.value,
                'ctime': now,
                'mtime': now,
            }, 't_user')
            user.id = id_
        else:
            user_table = Table('t_user')
            query = Query\
                .update(user_table)\
                .set(user_table.activate_code, user.activate_code)\
                .set(user_table.email, user.email)\
                .set(user_table.nickname, user.nickname)\
                .set(user_table.password_hash, user.password_hash) \
                .set(user_table.salt, user.salt) \
                .set(user_table.status, user.status.value)\
                .set(user_table.mtime, now)\
                .where(user_table.id == user.id)
            sql = query.get_sql(quote_char=None)
            self.execute_sql(sql)

        return self.get_by_email(user.email)

    def clear(self):
        """
        清空整个t_user表，用于单元测试的初始化。
        """
        user_table = Table('t_user')
        query = Query\
            .from_(user_table)\
            .delete()
        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

    def find(self, *, page: int, per_page: int) -> List[User]:
        """分页搜索用户集合。"""
        user_table = Table('t_user')
        query = Query\
            .from_(user_table)\
            .select(user_table.star)\
            .limit(per_page)\
            .offset((page - 1) * per_page)
        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                users = []
                for row in rows:
                    user = User()
                    user.activate_code = row['activate_code']
                    user.email = row['email']
                    user.id = row['id']
                    user.nickname = row['nickname']
                    user.password_hash = row['password_hash']
                    user.salt = row['salt']
                    user.status = UserStatus(row['status'])
                    users.append(user)

                return users

    def get_by_email(self, email: str) -> Union[User, None]:
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `t_user` WHERE `email` = %s"
                cursor.execute(sql, (email,))
                row = cursor.fetchone()
                if row is None:
                    return None

                user = User()
                user.activate_code = row['activate_code']
                user.email = row['email']
                user.id = row['id']
                user.nickname = row['nickname']
                user.password_hash = row['password_hash']
                user.salt = row['salt']
                user.status = UserStatus(row['status'])
                return user

    def remove(self, user: Union[User, int]):
        if isinstance(user, User):
            user_id = user.id
        else:
            assert isinstance(user, int)
            user_id = user

        self.remove_from_db(user_id, 't_user')

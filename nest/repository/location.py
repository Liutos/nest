# -*- coding: utf8 -*-
from typing import List, Union

from pypika import Query, Table

from nest.app.entity.location import ILocationRepository, Location
from nest.repository.db_operation import DatabaseOperationMixin


class DatabaseLocationRepository(DatabaseOperationMixin, ILocationRepository):
    def __init__(self, *, connection):
        super(DatabaseLocationRepository, self).__init__(connection)

    def add(self, *, location: Location):
        """将地点存储到数据库中。"""
        id_ = self.insert_to_db({
            'name': location.name,
            'user_id': location.user_id,
        }, 't_location')
        location.id = id_

    def clear(self):
        location_table = Table('t_location')
        query = Query\
            .from_(location_table)\
            .delete()
        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

    def find(self, *, ids: Union[None, List[int]] = None,
             name: Union[None, str] = None, page: int, per_page: int, user_id: int):
        """列出属于特定用户的地点。"""
        location_table = Table('t_location')
        query = Query\
            .from_(location_table)\
            .select(location_table.star)\
            .where(location_table.user_id == user_id)
        if ids is not None:
            query = query.where(location_table.id.isin(ids))
        if name is not None:
            query = query.where(location_table.name == name)

        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                return [self._row2entity(row) for row in rows]

    def get(self, *, id_: int) -> Union[None, Location]:
        """找出指定地点。"""
        location_table = Table('t_location')
        query = Query\
            .from_(location_table)\
            .select(location_table.star)\
            .where(location_table.id == id_)
        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                row = cursor.fetchone()
                if row is None:
                    return None

                return self._row2entity(row)

    def get_default(self, *, user_id: int) -> Union[None, Location]:
        """找出属于特定用户的默认地点。"""
        location_table = Table('t_location')
        query = Query\
            .from_(location_table)\
            .select(location_table.star)\
            .where(location_table.name == 'anywhere')\
            .where(location_table.user_id == user_id)
        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                location_dict = cursor.fetchone()
                if location_dict is None:
                    return None

                return self._row2entity(location_dict)

    def remove(self, *, id_: int):
        location_table = Table('t_location')
        query = Query\
            .from_(location_table)\
            .where(location_table.id == id_)\
            .delete()
        sql = query.get_sql(quote_char=None)
        with self.get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)

    def _row2entity(self, row: dict):
        return Location.new(
            id_=row['id'],
            name=row['name'],
            user_id=row['user_id'],
        )

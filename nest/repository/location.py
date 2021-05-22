# -*- coding: utf8 -*-
from typing import Union

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

                location = Location.new(
                    id_=location_dict['id'],
                    name=location_dict['name'],
                    user_id=location_dict['user_id'],
                )
                return location

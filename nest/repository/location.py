# -*- coding: utf8 -*-
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

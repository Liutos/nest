# -*- coding: utf8 -*-
class DatabaseOperationMixin:
    def __init__(self, connection):
        self.connection = connection

    def insert_to_db(self, kvs: dict, table_name: str) -> int:
        sql = 'INSERT INTO `{}` SET'.format(table_name)
        values = []
        is_first = True
        for column_name, value in kvs.items():
            if is_first:
                separator = ' '
            else:
                separator = ', '
            sql += '{}`{}` = %s'.format(separator, column_name)
            values.append(value)
            if is_first:
                is_first = False
        with self.connection.cursor() as cursor:
            cursor.execute(sql, tuple(values))
            inserted_id = cursor.lastrowid
        self.connection.commit()
        return inserted_id

    def remove_from_db(self, id_: int, table_name: str):
        with self.connection.cursor() as cursor:
            sql = 'DELETE FROM `{}` WHERE `id` = %s'.format(table_name)
            cursor.execute(sql, (id_,))
        self.connection.commit()

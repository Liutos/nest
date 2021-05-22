# -*- coding: utf8 -*-
from nest.app.entity.location import Location


class LocationPresenter:
    def __init__(self, *, location: Location):
        self.location = location

    def format(self):
        return {
            'id': self.location.id,
            'name': self.location.name,
            'user_id': self.location.user_id,
        }

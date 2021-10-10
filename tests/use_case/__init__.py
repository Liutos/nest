from typing import Union, List

from nest.app.entity.location import ILocationRepository, Location


class EmptyLocationRepository(ILocationRepository):
    def add(self, *, location: Location):
        pass

    def clear(self):
        pass

    def find(self, *, ids: Union[None, List[int]] = None,
             name: Union[None, str] = None, page: int, per_page: int, user_id: int):
        pass

    def get(self, *, id_: int) -> Union[None, Location]:
        pass

    def get_default(self, *, user_id: int) -> Union[None, Location]:
        pass

    def remove(self, *, id_: int):
        pass
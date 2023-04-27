# -*- coding: utf8 -*-
from typing import Optional, Union

from flask import request

from nest.app.use_case.authenticate import IParams


class CookiesParams(IParams):
    def get_certificate_id(self) -> Union[None, str]:
        return request.cookies.get('certificate_id')

    def get_email(self) -> Optional[str]:
        authorization = request.authorization
        return authorization and authorization.username

    def get_password(self) -> Optional[str]:
        authorization = request.authorization
        return authorization and authorization.password

    def get_user_id(self) -> Union[None, int]:
        user_id = request.cookies.get('user_id')
        return user_id and int(user_id)

# -*- coding: utf8 -*-
from nest.service.mail import SinaMailService


class ServiceFactory:
    # TODO: 之后补上对 config 的 type hint。
    def __init__(self, *, config):
        self.config = config

    def mail(self) -> SinaMailService:
        mail_section = self.config['mail']
        return SinaMailService(
            password=mail_section['password'],
            user=mail_section['user'],
        )

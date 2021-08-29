# -*- coding: utf8 -*-
from nest.app.use_case.registration import IMailService


class MockMailService(IMailService):
    def send_activate_code(self, *, activate_code: str, email: str):
        pass

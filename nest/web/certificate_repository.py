# -*- coding: utf8 -*-
from nest.repository.certificate import RedisCertificateRepository
from nest.web.config import config

redis_section = config['redis']
db = int(redis_section['db'])
host = redis_section['host']
port = int(redis_section['port'])
certificate_repository = RedisCertificateRepository(
    db=db,
    host=host,
    port=port
)

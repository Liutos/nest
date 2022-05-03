# -*- coding: utf8 -*-
from nest.repository.certificate import RedisCertificateRepository
from nest.web import config


_the_repository = None


def get_repository():
    """提供全局唯一的证书 repository 对象的访问入口。"""
    global _the_repository
    if _the_repository is None:
        redis_section = config.get_config()['redis']
        db = int(redis_section['db'])
        host = redis_section['host']
        port = int(redis_section['port'])
        _the_repository = RedisCertificateRepository(
            db=db,
            host=host,
            port=port
        )

    return _the_repository

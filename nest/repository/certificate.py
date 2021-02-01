# -*- coding: utf8 -*-
import redis

from nest.app.entity.certificate import Certificate, ICertificateRepository

_count = 0
_user_certificates = {}


class MemoryCertificateRepository(ICertificateRepository):
    def __init__(self):
        global _count
        global _user_certificates
        self.count = _count
        self.user_certificates = _user_certificates

    def add(self, certificate: Certificate):
        """
        将登录凭证保存在内存中。
        """
        certificate.id = self._get_next_id()
        user_certificates = self.user_certificates
        user_certificates[certificate.user_id] = certificate

    def get_by_certificate_id(self, certificate_id: int) -> Certificate:
        for _, certificate in self.user_certificates.items():
            if certificate.id == certificate_id:
                return certificate
        return None

    def _get_next_id(self):
        global _count
        next_id = self.count
        self.count += 1
        _count += 1
        return next_id


class RedisCertificateRepository(ICertificateRepository):
    def __init__(self, *, db: int, host: str, port: int):
        self.client = redis.Redis(
            db=db,
            host=host,
            port=port,
        )

    def add(self, certificate: Certificate):
        """
        将登录凭证保存在Redis中。
        """
        id_ = self._get_next_id()
        certificate.id = id_
        name = 'nest:user:certificate:{}'.format(id_)
        self.client.hset(name, 'user_id', certificate.user_id)

    def get_by_certificate_id(self, certificate_id: int) -> Certificate:
        name = 'nest:user:certificate:{}'.format(certificate_id)
        user_id = int(self.client.hget(name, 'user_id'))
        print('user_id', user_id)
        certificate = Certificate()
        certificate.id = certificate_id
        certificate.user_id = user_id
        return certificate

    def _get_next_id(self):
        name = 'nest:certificate:id'
        return int(self.client.incr(name))

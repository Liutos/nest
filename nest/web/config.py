# -*- coding: utf8 -*-
"""提供应用配置的全局唯一访问入口。"""
import os

from nest.infra.config import Config


def _load_config():
    current_dir = os.path.dirname(__file__)
    config_dir = os.path.join(current_dir, './config')
    file_name = os.environ.get('MODE', 'default')
    config_file = os.path.join(config_dir, file_name + '.ini')
    return Config(config_file)


_the_config = None


def get_config():
    """返回加载完成的应用配置对象。

如果配置尚未加载，将会加载一次供后续使用。"""
    global _the_config
    if _the_config is None:
        _the_config = _load_config()

    return _the_config

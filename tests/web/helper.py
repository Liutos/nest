# -*- coding: utf8 -*-
import os


def get_config_file_path():
    current_dir = os.path.dirname(__file__)
    print('current_dir', current_dir)
    config_dir = os.path.join(current_dir, '../../nest/web/config')
    file_name = 'default'
    mode = os.environ.get('MODE')
    if mode == 'unittest':
        file_name = 'unittest'
    return os.path.join(config_dir, file_name + '.ini')

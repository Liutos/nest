# -*- coding: utf8 -*-
import configparser
import os

config = configparser.ConfigParser()
current_dir = os.path.dirname(__file__)
config_dir = os.path.join(current_dir, './config')
file_name = 'default'
mode = os.environ.get('MODE')
if mode == 'unittest':
    file_name = 'unittest'
config_file = os.path.join(config_dir, file_name + '.ini')
print('config_file', config_file)
config.read(config_file)
print('config.sections()', config.sections())

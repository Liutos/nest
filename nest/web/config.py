# -*- coding: utf8 -*-
import configparser
import os


class Config:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        print('config_file', config_file)
        config.read(config_file)
        print('config.sections()', config.sections())
        self.config = config

    def __getitem__(self, item):
        return self.config[item]

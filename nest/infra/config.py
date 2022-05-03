# -*- coding: utf8 -*-
import configparser


class Config:
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        self.config = config

    def __getitem__(self, item):
        return self.config[item]

# coding:utf8
from __future__ import absolute_import

import json
import logging
import os


class Config(object):
    pass


CONFIG = Config()


def init_config(json_dict):
    CONFIG.__dict__ = json_dict


def load_config():
    pwd = os.path.dirname(__file__)
    config_file = os.path.join(pwd, "env.json")
    config_dict = json.load(open(config_file))
    init_config(config_dict)

    logging.info("------current environment is \"%s\","
                 "using config file: \"%s\"" % (CONFIG.ENV, config_file))

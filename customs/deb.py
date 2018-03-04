'''
Module for installing and setting up debian packages
'''

import os
from subprocess import Popen, PIPE

from constants import *
from helpers import Helpers as h, c_logger, v_logger

class Deb():

    def __init__(self, config_location='ides'+PACKAGE_EXTENSION):
        self.config_location = config_location

    def run(self):
        v_logger(h.LOG_MODE.INFO, 'Parsing DEBs...')
        deb_settings = h.parse_json(self.config_location)
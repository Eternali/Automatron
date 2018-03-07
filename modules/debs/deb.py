'''
Module for installing and setting up debian packages.
The packages can either be stored locally already, ore fetched remotely.

(C) Conrad Heidebrecht (github.com/eternali) 04 March 2018
'''

import os
from subprocess import Popen, PIPE
import sys
from types import SimpleNamespace as Sn
import urllib.request

# get abspath of this file and go one directory up and append it to sys path
sys.path.append(os.path.abspath(__file__).rsplit(os.sep, 2)[0])

from constants import *
from helpers import Helpers as h, c_logger, v_logger

class Deb():

    def __init__(self, config_location='deb'+PACKAGE_EXTENSION):
        self.config_location = config_location

    def run(self):
        v_logger(h.LOG_MODE.INFO, 'Parsing DEBs...')
        deb_settings = h.parse_json(self.config_location)

        local_base = deb_settings['local_base'] # base dir of predownloaded DEB packages
        download_base = deb_settings['download_base'] # base dir to download remote DEBs to
        install_cmd = deb_settings['install_cmd']
        
        for deb in deb_settings['debs']:
            # load source package (if remote download and resolve local name)
            v_logger(h.LOG_MODE.INFO, '{}: Retrieving debian package.'.format(deb['name']))
            deb_location = ''
            if len([deb['source'].startswith(proto) for proto in SUPPORTED_PROTOCOLS]):
                deb_location = download_base + os.sep + deb['name'] + '.deb'
                c_logger()
                urllib.request.urlretrieve(deb['source'], deb_location)
            else:
                deb_location = local_base + os.sep + deb['name'] + '.deb'

            # install package using deb location
            Popen([install_cmd, deb_location], stdout=PIPE)

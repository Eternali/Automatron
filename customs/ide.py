'''
Module for installing and setting up common ides whose install format is based on
extracting a zipped archive and running the ide script with config saved to a directory
(usually in a .`ide_name` folder in the user's home directory). 
    e.g. Intellij based ides like Pycharm, Clion, Android Studio, and more...

(C) Conrad Heidebrecht (github.com/eternali) 04 February 2018
'''

import os
from subprocess import Popen, PIPE
import shutil
import sys
import tarfile
from types import SimpleNamespace as Sn
import zipfile

sys.path.insert(0, '../')

from constants import *
from helpers import Helpers as h, c_logger, v_logger


class Ide():

    def __init__(self, config_location="ide"+PACKAGE_EXTENSION):
        self.config_location = config_location

    def run(self):
        v_logger(h.LOG_MODE.INFO, 'Parsing IDEs..')
        ide_settings = h.parse_json(self.config_location)
        custom_base = custom['custom_base']
        install_base = custom['install_base']
        
        for ide in ide_settings['ides']:
            # get application locations
            v_logger(h.LOG_MODE.INFO, 'Parsing {} config.'.format(ide['name']))
            archive_location = custom_base if ide['archive_location'].startswith('~') else '' + arch['archive_location']
            install_location = install_base if ide['install_location'].startswith('~') else '' + ide['install_location']
            
            # get application config locations
            config_origin = ide['config_origin'] if 'config_origin' in ide.keys() else None
            config_save = ide['config_save'] if 'config_save' in ide.keys() else None

            # check how to install it
            archivetype = h.filetype(archive_location)
            v_logger(h.LOG_MODE.INFO, '{}: Extracting {} to {}..'.format(ide['name'], archive_location, install_location))
            if archivetype in FILETYPES.TGZ + FILETYPES.TXZ:
                c_logger(Sn(stringify=lambda: '''
                        gzipped = tarfile.open(archive_location)
                        gzipped.extractall(path=install_location)
                        gzipped.close()
                        '''.strip(' '),
                            run=lambda: (
                                gzipped = tarfile.open(archive_location)
                                gzipped.extractall(path=install_location)
                                gzipped.close()
                        )))
                gzipped = tarfile.open(archive_location)
                gzipped.extractall(path=install_location)
                gzipped.close()
            elif archivetype in FILETYPES.ZIP:
                c_logger(Sn(stringify=lambda: ,
                            run=lambda: ))
                zipped = zipfile.open(archive_location)
                zipped.extractall(path=install_location)
                zipped.close()
            elif archivetype in FILETYPES.DEB:
                c_logger(Sn(stringify=lambda: ' '.join(['dpkg', '-i', archive_location]),
                            run=lambda: Popen(['dpkg', '-i', archive_location], stdout=PIPE).wait()), 0)

            # config copying/installation
            v_logger(h.LOG_MODE.INFO, '{}: Copying config files'.format(ide['name']))
            if os.path.exists(config_origin) and config_save:
                c_logger(Sn(stringify=lambda: 'shutil.copytree(config_origin, config_save)',
                            run=lambda: shutil.copytree(config_origin, config_save)))


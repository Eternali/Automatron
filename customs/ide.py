'''

'''

import os
import subprocess
import shutil
import tarfile
import zipfile

from helpers import Helpers as h
from constants import *


class Ide():

    def __init__(self, config_location="ides"+PACKAGE_EXTENSION):
        self.config_location = config_location

    def run(self):
        ide_settings  = h.parse_json(self.config_location)
        custom_base = custom['custom_base']
        install_base = subarchive['install_base']
        
        for ide in ide_settings['ides']:
            # get application locations
            archive_location = custom_base if ide['archive_location'].startswith('~') else '' + arch['archive_location']
            install_location = install_base if ide['install_location'].startswith('~') else '' + ide['install_location']
            
            # get application config locations
            config_origin = ide['config_origin'] if 'config_origin' in ide.keys() else None
            config_save = ide['config_save'] if 'config_save' in ide.keys() else None
            
            # check how to install it
            archivetype = h.filetype(archive_location)
            if archivetype in FILETYPES.TGZ + FILETYPES.TXZ:
                gzipped = tarfile.open(archive_location)
                gzipped.extractall(path=install_location)
                gzipped.close()
            elif archivetype in FILETYPES.ZIP:
                zipped = zipfile.open(archive_location)
                zipped.extractall(path=install_location)
                zipped.close()
            elif archivetype in FILETYPES.DEB:
                subprocess.Popen(['dpkg', '-i', archive_location], stdout=subprocess.PIPE).wait()

            # config copying/installation
            if os.path.exists(config_origin) and config_save:
                shutil.copytree(config_origin, config_save)




'''
Globals contains global constants for ATO and custom modules
This does not contain any methods (all methods should go in helpers.py)

(C) Conrad Heidebrecht (github.com/eternali) 03 February 2018

'''

from enum import Enum


# these are the only values that can be changed by commandline arguments
DRY_RUN = False
VERBOSE = False

PACKAGE_DIR = 'packages/'
CUSTOM_DIR = 'customs.'
PACKAGE_EXTENSION = '.json'

class COLORS(Enum):
    RED = ''
    GREEN = ''
    BLUE = ''
    PURPLE = ''
    CYAN = ''

class FILETYPES(Enum):
    TGZ = ['gzip, tar.gz']
    TXZ = ['x-xz', 'xzip', 'tar.xz']
    ZIP = ['zip']
    DEB = ['deb', 'debian', 'vnd.debian.binary-package']

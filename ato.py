#!/usr/bin/python3
'''

(C) Conrad Heidebrecht (github.com/eternali) 07 March 2018

'''

#-----------PYTHON STANDARD IMPORTS----------
from importlib import import_module
import os
from subprocess import Popen, PIPE
from sys import argv

#-----------PACKAGE IMPORTS------------------
import config as c
from helpers import Helpers as H, Command as Cmd, LOG_MODE


#-----------HELPER FUNCTIONS-----------------
def usage():
    print('''

Automatron is an extensible script that is meant to simplify the setup of new linux machines.
It provides an interface to automate the installation of files such as debian, npm, or pip packages,
as well as more complex and customizable applications such as IDE's and any number of other groups
of packages that share installation features.

Several modules are provided with Automatron by default, these include modules for installing 
apt, pip and npm packages with several sample packages configured for install.
It is intended that the user provide additional modules as they need,
the format of each additional module must be as follows:

- a python file containing a single class (the name of the module)
- the name of the file must match the lowercase name of the class.
- the only requirements of the class are that:
    a. it's constructor takes an instance of the Helpers class as its only parameter
    b. it has a run method which takes the following parameters:
        - progress (float): shared progress value (to increment)
        - interactive (bool): interactivity flag the module can use to allow the user to interact with
          the module. e.g. launch an interactive prompt to allow the user to perform commands to
          add/remove/modify package installation configuration.
- Note: It is up to individual modules to know their location on the filesystem relative to Ato
    (this is important if modules need to import configuration from Ato).
- though not a requirement, it is recommended that each module contain one or more JSON file(s)
    to store configuration and data.
- though not a requirement, it is recommended that modules be placed in a subdirectory of Ato so as to
    enable easier use of the configuration and helpers provided by Ato.
- though not a requirement, it is recommended that modules follow the following structure:
    a. JSON files are used to store module-wide configuration and a list of packages to install and/or setup
    b. Package archives and/or configuration to install are either stored in a separate data directory,
        or a remote location.
    c. Parse configuration and packages from JSON file(s)
    d. Loop through each package and install it using module and package specific configuration.


./ato.py [-d --dry-run] [-v --verbose] [-i --interactive] [-h --help] [modules]

    [-d --dry-run]     Only log commands instead of actually running them,
                       modules must specify their own dry run processes,
                       in addition to the basic core command logging one provided by ato.py
                           e.g. A 'apt' module might additionally specify that each package install command
                           should be completed with the '--dry-run' option to simulate installation
    [-v --verbose]     Log extra commands and display additional information
    [-i --interactive] Run modules in interactive mode (implementation depends on the module, see above for details)
    [-h --help]        Show this help
    [modules]          A space separated list of modules to configure,
                           entries consist of either a path to a specific module,
                           or a path to a directory containing one or more modules
                           e.g. 'modules/deb'


        ''')


def check_user(uid=1000):
    return os.getuid() == uid

# strip '.py' from files and replace '/' with '.' 
# (that's how file hierarchy is specified in python modules)
def to_module(name):
    if name.endswith('.py'):
        return name.rsplit('.', 1)[0].replace(os.sep, '.')
    return name

def is_module(name):
    if os.path.isfile(name):
        return 'python' in H.filetype(name)
    return False

def get_modules(name):
    modules = []
    if os.path.isdir(name):
        for root, _, files in os.walk(name):
            modules += [to_module(os.path.join(root, fname)) for fname in files if is_module(os.path.join(root, fname))]

    return modules

def parse_args(args):

    def in_args(flags):
        return any([f in args for f in flags])

    if in_args(['-h', '--help']) or len(args) < 1:
        usage()
        quit(0)

    return (H(in_args(['-d', '--dry-run']), in_args(['-v', '--verbose'])), in_args(['-i', '--interactive']),
           [m for sm in [[to_module(a)] if is_module(a) else get_modules(a) for a in args if not a.startswith('-')] for m in sm])


#-----------MAIN ENTRYPOINT------------------
if __name__ == '__main__':

    # overall progress value that can be passed to modules to increment
    progress = 0.0

    h, interactive, modules = parse_args(argv[1:])
    print(modules)

    for module in modules:
        h.logger(LOG_MODE.INFO, 'Loading module ' + module)
        importer = import_module(module)
        loader = getattr(importer, module.split('.')[-1].capitalize())(h)
        loader.run(progress, interactive)

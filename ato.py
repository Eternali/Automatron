#!/usr/bin/python3
'''

'''

#-----------PYTHON STANDARD IMPORTS----------
from importlib import import_module
import os
import subprocess
import sys

#-----------PACKAGE IMPORTS------------------
from constants import *
from helpers import Helpers as h, v_logger


#-----------HELPER FUNCTIONS-----------------


def usage():
    print('''
        ./ato.py [-p --packages] pack1 pack2 [-c --customs] custom1:install_module1 custom2:install_module2

            [-p --packages]  install packages from common package managers (e.g. apt, pacman, pip, npm)
            [-c --customs]   install custom items from archives or other sources. The first item is the JSON
                             file that specifies things like archive locations, configuration, and other data
                             for the install. The second item is a python module you must provide to parse the 
                             JSON file you provide.
                             The python module must be a single class with the same name as the file and must
                             contain a `run` method that will be called by ATO.
        ''')


def check_user(uid=1000):
    return os.getuid() == uid


def get_named_args(aliases):
    argv = sys.argv[1:]
    alias_idx = []
    for alias in aliases:
        arg_idx = [argv.index(a) if a in argv else -1 for a in alias]
        if arg_idx.count(-1) != len(arg_idx) - 1:
            usage()
        alias_idx.append([a for a in arg_idx if a != -1][0])

    return [argv[alias_idx[i]+1:alias_idx[i+1] if len(alias_idx) > i+1 else len(argv)] for i in range(len(alias_idx))]


#-----------MAIN ENTRYPOINT------------------

if __name__ == '__main__':

    # progress value that can be passed to modules to increment
    progress = 0

    # check if we're running in dry-run mode
    # this will log all the commands that we would execute as well as actually running
    # commands that have specific dry-run configuration (e.g. apt's `--dry-run` flag)
    if '-d' in sys.argv:
        DRY_RUN = True
        sys.argv.remove('-d')
    else:
        DRY_RUN = False

    # check if we want to be in verbose mode (log all that we're doing)
    if '-v' in sys.argv:
        VERBOSE = True
        sys.argv.remove('-v')
    else:
        VERBOSE = False

    packages, customs = get_named_args([('-p', '--packages'), ('-c', '--customs')])
    print(packages)
    print(customs)


    # execute common package installations

    for pack in packages:
        v_logger(h.LOG_MODE.INFO, 'Parsing {} {}..'.format(pack, PACKAGE_EXTENSION.strip('.').upper()))
        package = h.parse_json(PACKAGE_DIR + pack + PACKAGE_EXTENSION)
        manager, install_cmd, items, dry_cmd = (package['package_manager'],
                                                package['install_cmd'],
                                                package['packages'],
                                                package['dry_run'] if 'dry_run' in file_dict.keys() else '')
        # execute prerequesites for package installs
        for item in items:
            if "prereq" in item.keys():
                v_logger(h.LOG_MODE.INFO, '{}: Executing prerequesites for {}..'.format(pack, item['name']))
                if subprocess.Popen(' && '.join(item['prereq'])).wait() != 0:
                    v_logger(h.LOG_MODE.ERR, '{}: Failed to execute prerequesites of {}'.format(pack, item['name']))
                    raise Exception('Failed to execute prerequesites of {} from package {}'.format(item['name'], pack))
        # execute final package installations
        v_logger(h.LOG_MODE.INFO, '{}: Installing all packages..'.format(pack))
        if subprocess.Popen([install_cmd, dry_cmd if dry_run else ''] + [item['name'] for item in items]).wait() != 0:
            v_logger(h.LOG_MODE.ERR, '{}: Failed to install packages.'.format(pack))
            raise Exception('Failed to complete installation of {}.'.format(pack))


    # load and run custom modules
    for custom in customs:
        v_logger(h.LOG_MODE.INFO, 'Loading module {}'.format(custom))
        custom_mod = import_module(CUSTOM_DIR + custom)
        Custom = getattr(custom_mod, custom.title())
        c = Custom()
        v_logger(h.LOG_MODE.INFO, 'Running module {}'.format(custom))
        c.run()

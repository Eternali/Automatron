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
from helpers import Helpers as h


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

    # check if we're running in testing mode
    if '-d' in sys.argv:
        dry_run = True
        sys.argv.remove('-d')
    else:
        dry_run = False

    packages, customs = get_named_args([('-p', '--packages'), ('-c', '--customs')])
    print(packages)
    print(customs)


    # execute common package installations

    for pack in packages:
        package = h.parse_json(PACKAGE_DIR + pack + PACKAGE_EXTENSION)
        manager, install_cmd, items, dry_cmd = (package['package_manager'],
                                                package['install_cmd'],
                                                package['packages'],
                                                package['dry_run'] if 'dry_run' in file_dict.keys() else '')
        # execute prerequesites for package installs
        for item in items:
            if "prereq" in item.keys():
                if subprocess.Popen(' && '.join(item['prereq'])).wait() != 0:
                    raise Exception('Failed to complete prerequesites of {} from package {}'.format(item['name'], manager))
        # execute final package installations
        if subprocess.Popen([install_cmd, dry_cmd if dry_run else ''] + [item['name'] for item in items]).wait() != 0:
            raise Exception('Failed to complete installation of {}.'.format(manager))


    # load and run custom modules
    for custom in customs:
        custom_mod = import_module(CUSTOM_DIR + custom)
        Custom = getattr(custom_mod, custom.title())
        c = Custom()
        c.run()            

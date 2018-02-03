'''

'''

#-----------PYTHON STANDARD IMPORTS----------
import json
# import operator
import os
import subprocess
import sys

#-----------PACKAGE IMPORTS------------------


#-----------GLOBAL CONSTANTS-----------------
PACKAGE_DIR = 'packages/'
CUSTOM_DIR = 'customs/'
PACKAGE_EXTENSION = '.json'


#-----------HELPER FUNCTIONS-----------------

def usage():
    print('''
        ./ato.py [-p --packages] pack1 pack2
        ''')


def check_user(uid=1000):
    return os.getuid() == uid


def check_permissions(target=755):
    pass


def filetype(filename):
    pass


def get_named_args(aliases):
    argv = sys.argv[1:]
    alias_idx = []
    for alias in aliases:
        arg_idx = [argv.index(a) if a in argv else -1 for a in alias]
        if arg_idx.count(-1) != len(arg_idx) - 1:
            usage()
        alias_idx.append([a for a in arg_idx if a != -1][0])

    return [argv[alias_idx[i]+1:alias_idx[i+1] if len(alias_idx) > i+1 else len(argv)] for i in range(len(alias_idx))]


def parse_json(filename):
    with open(filename, 'r') as fname:
        loaded_file = fname.read()
    file_dict = json.loads(loaded_file)
    return file_dict


def write_json(dict_to_encode, filename, separators=(',', ':')):
    with open(filename, 'w') as fname:
        fname.write(json.dumps(dict_to_encode, indent=2, separators=separators))


def organize_dict(items, key, applicator=None):
    sorted_dict = []
    if applicator is None:
        sorted_dict = sorted(items, key=lambda k: k[key])
        # items.sort(key=operator.itemgetter('name'))
    return sorted_dict


#-----------MAIN ENTRYPOINT------------------

if __name__ == '__main__':

    # check if we're running in testing mode
    if '-d' in sys.argv:
        dry_run = True
        sys.argv.remove('-d')
    else:
        dry_run = False

    packages, archives = get_named_args([('-p', '--packages'), ('-a', '--archives')])
    print(packages)
    print(archives)


    # execute common package installations

    for pack in packages:
        package = parse_json(PACKAGE_DIR + pack + PACKAGE_EXTENSION)
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


    # installing applications from archives
    for arch in archives:
        archive = parse_json(CUSTOM_DIR + arch + PACKAGE_EXTENSION)
        working_dir = archive['working_dir']
        if filetype(archive_location) == FILETYPES.TGZ:
            pass

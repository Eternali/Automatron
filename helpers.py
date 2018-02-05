'''
Helpers contains only static methods that ATO or custom modules can import.

(C) Conrad Heidebrecht (github.com/eternali) 03 February 2018
'''


from enum import Enum
import json
import magic
import os
import stat

from constants import *


# command logging for dry-run mode
# cmd is an object that has a to_string method to print
# and a run method to execute
def c_logger(cmd, expected=0):
    if DRY_RUN:
        Helpers.logger(Helpers.LOG_MODE.CMD, cmd.stringify())
        return expected
    else:
        return cmd.run() == expected


# logger for verbose mode
def v_logger(mode, body):
    if VERBOSE:
        Helpers.logger(mode, body)


class Helpers():

    class LOG_INFO():
        def __init__(prefix, suffix, color):
            self.prefix = prefix
            self.suffix = suffix
            self.color = color
            self.reset = ''

    class LOG_MODE(Enum):
        INFO = LOG_INFO('[**] ', '.', COLORS.BLUE)
        ERR = LOG_INFO('[!!] ', '!', COLORS.RED)
        PASS = LOG_INFO('[//] ', '!', COLORS.GREEN)
        CMD = LOG_INFO('[$$] ', ';', COLORS.PURPLE)
        OTHER = LOG_INFO('[~^] ', '.', COLORS.CYAN)

    @staticmethod
    def logger(mode, body):
        if type(mode) is LOG_MODE:
            print(mode.color + mode.prefix + body + mode.suffix + mode.reset)
        else:
            raise TypeError('Invalid log mode!')

    @staticmethod
    def check_permissions(target, perm=755, fix=False):
        correct = int(oct(stat.S_IMODE(os.stat(target).st_mode))[-3:]) == perm
        if not correct and fix:
            if VERBOSE:

            if not DRY_RUN:
                os.chmod(target, perm)
        else:
            return correct

    @staticmethod
    def filetype(filename, parser=lambda string: string.split('/')[-1]):
        type_str = magic.from_file(filename, mime=True)
        return parser(type_str)

    @staticmethod
    def parse_json(filename):
        with open(filename, 'r') as fname:
            loaded_file = fname.read()
        file_dict = json.loads(loaded_file)
        return file_dict

    @staticmethod
    def write_json(dict_to_encode, filename, separators=(',', ':')):
        with open(filename, 'w') as fname:
            fname.write(json.dumps(dict_to_encode, indent=2, separators=separators))

    @staticmethod
    def organize_dict(items, key, applicator=None):
        sorted_dict = []
        if applicator is None:
            sorted_dict = sorted(items, key=lambda k: k[key])
        return sorted_dict

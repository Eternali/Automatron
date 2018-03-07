'''
Helpers contains helper classes and methods that ATO or custom modules can import.

(C) Conrad Heidebrecht (github.com/eternali) 07 March 2018
'''


from enum import Enum
import json
import magic
import os
import stat

from config import *


# Command class for executing loggable commands
# if you want to log commands for debug, dry-run, or verbosity purposes, use this class
# 'run' is the expression/function to execute and 'str' is the string to print out
class Command():
    __slots__ = ['run', 'stringify']

    def __init__(self, run, stringify):
        self.run = run
        self.stringify = stringify


class Helpers():

    class LOG_INFO():
        def __init__(self, prefix, suffix, color):
            self.prefix = prefix
            self.suffix = suffix
            self.color = color
            self.reset = ''

    class LOG_MODE(Enum):
        INFO = Helpers.LOG_INFO('[**] ', '.', COLORS.BLUE)
        ERR = Helpers.LOG_INFO('[!!] ', '!', COLORS.RED)
        PASS = Helpers.LOG_INFO('[//] ', '!', COLORS.GREEN)
        CMD = Helpers.LOG_INFO('[$$] ', ';', COLORS.PURPLE)
        OTHER = Helpers.LOG_INFO('[~^] ', '.', COLORS.CYAN)

    @staticmethod
    def logger(mode, body):
        if type(mode) is Helpers.LOG_MODE:
            print(mode.color + mode.prefix + body + mode.suffix + mode.reset)
        else:
            raise TypeError('Invalid log mode!')

    # command logging for dry-run mode
    # cmd must be an instance of Command
    @staticmethod
    def c_logger(cmd, expected=0):
        if type(cmd) is Command:
            if DRY_RUN:
                Helpers.logger(Helpers.LOG_MODE.CMD, cmd.str)
                return expected
            else:
                return cmd.run() == expected
        else:
            raise TypeError('Cmd not of type Command')

    # logger for verbose mode
    @staticmethod
    def v_logger(mode, body):
        if VERBOSE:
            Helpers.logger(mode, body)

    @staticmethod
    def check_permissions(target, perm=755, fix=False):
        correct = int(oct(stat.S_IMODE(os.stat(target).st_mode))[-3:]) == perm
        if not correct:
            if fix:
                Helpers.v_logger(Helpers.LOG_MODE.INFO, target + ' does not have target permissions of ' + perm + ', fixing.')
                return Helpers.c_logger(Command(lambda: os.chmod(target, perm), 'os.chmod(%s, %i)' % (target, perm)))
            else:
                Helpers.v_logger(Helpers.LOG_MODE.ERR, target + ' does not have target permissions of ' + perm + ', not fixing.')
                return True

        return correct

    @staticmethod
    def filetype(filename, parser=lambda string: string.split(os.sep)[-1]):
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

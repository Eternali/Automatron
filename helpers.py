'''
Helpers contains helper classes and methods that ATO or custom modules can import.

(C) Conrad Heidebrecht (github.com/eternali) 07 March 2018
'''


from enum import Enum
import json
import magic
import os
import stat

import config as c


# Command class for executing loggable commands
# if you want to log commands for debug, dry-run, or verbosity purposes, use this class
# 'run' is the expression/function to execute and 'str' is the string to print out
class Command():
    __slots__ = ['run', 'stringify']

    def __init__(self, run, stringify):
        self.run = run
        self.stringify = stringify


class LOG_INFO():
    def __init__(self, prefix, suffix, color):
        self.prefix = prefix
        self.suffix = suffix
        self.color = color
        self.reset = ''


class LOG_MODE(Enum):
    INFO = LOG_INFO('[**] ', '.', c.COLORS.BLUE)
    ERR = LOG_INFO('[!!] ', '!', c.COLORS.RED)
    PASS = LOG_INFO('[//] ', '!', c.COLORS.GREEN)
    CMD = LOG_INFO('[$$] ', ';', c.COLORS.PURPLE)
    OTHER = LOG_INFO('[~^] ', '.', c.COLORS.CYAN)


class Helpers():
    
    def __init__(self, dry_run=False, verbose=False):
        self.dry_run = dry_run
        self.verbose = verbose

    def logger(self, mode, body):
        if type(mode) is LOG_MODE:
            mode = mode.value
            print(mode.color.value + mode.prefix + body + mode.suffix + mode.reset)
        else:
            raise TypeError('Invalid log mode!')

    # command logging for dry-run mode
    # cmd must be an instance of Command
    def c_logger(self, cmd, expected=0):
        if type(cmd) is Command:
            if self.dry_run:
                self.logger(LOG_MODE.CMD, cmd.stringify)
                return expected
            else:
                return cmd.run() == expected
        else:
            raise TypeError('Cmd not of type Command')

    # pretty print progress across bottom of screen
    # progress is a float between 0 and 1 (percentage)
    def p_logger(self, progress):
        pass

    # logger for verbose mode
    def v_logger(self, mode, body):
        if self.verbose:
            self.logger(mode, body)

    # log progress
    # progress is a floating point value between 0 and 100 (percentage)
    def p_logger(self, progress):
        print()

    def check_perms(self, target, perm=755, fix=False):
        correct = int(oct(stat.S_IMODE(os.stat(target).st_mode))[-3:]) == perm
        if not correct:
            if fix:
                self.v_logger(LOG_MODE.INFO, target + ' does not have target permissions of ' + perm + ', fixing.')
                return self.c_logger(Command(lambda: os.chmod(target, perm), 'os.chmod(%s, %i)' % (target, perm)))
            else:
                self.v_logger(LOG_MODE.ERR, target + ' does not have target permissions of ' + perm + ', not fixing.')
                return True

        return correct

    @staticmethod
    def filetype(filename, parser=lambda string: string.split(os.sep)[-1]):
        type_str = magic.from_file(filename, mime=True)
        return parser(type_str)

    @staticmethod
    def is_json(filename):
        '''
        Tests whether or not a file is JSON be checking first character
        THIS DOES NOT CHECK THE VALIDITY OF THE FILE

        :param filename (string): filename to check
        :returns: boolean whether the file is JSON or not
        '''
        with open(filename, 'r') as fname:
            for line in fname:
                if line.startswith('{'):
                    return True
                

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

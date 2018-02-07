'''

'''

import os


class PyParser():

    def __init__(self, load_file):
        self.__properties__ = {}
        if load_file is not None:
            self.load(load_file)

    def __setitem__(self, key, value):
        self.__properties__[key] = value

    def __getitem__(self, item):
        return self.__properties__.get(item)

    def load(self, filename):
        self.__properties__ = {}
        
        if not os.path.isfile(filename):
            return False
        
        with open(filename, 'rb') as f:
            for l in f:
                line = l.rstrip(os.linesep).strip('\t')
                if len(line) < 2 or '=' not in line or line.startswith('#'):
                    continue
                line = line.split('=', 1)
                key = line[0].strip()
                value = line[1].strip() if len(line) > 1 else ''
                self.parse_prop(self.__properties__, key.split('.'), value)
        
        return True

    def parse_prop(self, props, keys, value):
        if keys[0] in props.keys():
            self.parse_prop(props[keys[0]], keys[1:], value)
        elif len(keys) > 1:
            props[keys[0]] = {}
            self.parse_prop(props[keys[0]], keys[1:], value)
        else:
            props[keys[0]] = value

    def save_props(self, filename):
        pass


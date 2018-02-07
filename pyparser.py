'''
PropParser.py  ver. 0.1

(C) Conrad Heidebrecht (github.com/eternali) 07 Feb 2018


PropParser is a properties parser that explicitly supports hierarchical document structure.
Levels of property hierarchy is denoted by '.' in the property name.
For example:
    a.b = 12
    a.c=test
    d=321
will be parsed to a dictionary:
    {
        'a': {
            'b': '12',
            'c': 'test'
        },
        'd': 321
    }

You can nest as many levels as you like, however the root property of a hierarchy cannot be explicitly set.
For example the following will raise an error:
    a = 123
    a.b = test
This is because 'a' is initially set to an integer, but then wants to be reassigned to a dictionary.

*Note: Property metadata is not currently supported in this release.

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
        
        with open(filename, 'r') as f:
            for l in f:
                line = l.rstrip(os.linesep).strip('\t')
                if len(line) < 2 or '=' not in line or line.startswith('#'):
                    continue
                line = line.split('=', 1)
                key = line[0].strip()
                value = line[1].strip() if len(line) > 1 else ''
                self.__parse_prop(self.__properties__, key.split('.'), value)
        
        return True

    def __parse_prop(self, props, keys, value):
        if keys[0] in props.keys():
            self.__parse_prop(props[keys[0]], keys[1:], value)
        elif len(keys) > 1:
            props[keys[0]] = {}
            self.__parse_prop(props[keys[0]], keys[1:], value)
        else:
            props[keys[0]] = value

    def save(self, filename):
        filename = (os.getcwd() + '/' if not filename.startswith('/') else '') + filename
        if not os.path.exists(filename.rsplit('/', 1)[0]):
            os.makedirs(filename.rsplit('/', 1)[0])

        with open(filename, 'w+') as f:
            compiled = []
            self.__build(self.__properties__, '', compiled)
            f.write('\n'.join(compiled))

    def __build(self, prop, cur_line, compiled):
        if isinstance(prop, dict):
            for key in prop.keys():
                self.__build(prop[key], cur_line + ('.' if cur_line else '') + str(key), compiled)
        else:
            compiled.append(cur_line + '=' + prop)
        


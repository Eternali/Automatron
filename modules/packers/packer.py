'''


'''

import os
from subprocess import Popen, PIPE
import sys

# get abspath of this file and go two directories up and append it to sys path
sys.path.append(os.path.abspath(__file__).rsplit(os.sep, 3)[0])

import config as c


class Packer():

    def __init__(self, h):
        self.h = h
        self.work_dir = os.path.abspath(__file__).rsplit(os.sep, 1)[0]
        self.sources = [self.work_dir + os.sep + d for d in os.listdir(self.work_dir) if self.h.is_json(self.work_dir + os.sep + d)]

    def configure(self):
        

    def install(self, package, install_cmd, dry_cmd, packages=[]):
        if package.get('completed'):
            return package
            
        if 'deps' in package.keys():
            for dep in package['deps']:
                found_dep = [p for p in packages if p['name'] == dep]
                if not found_dep:
                    packages.append(self.install({ 'name': dep }, install_cmd, dry_cmd))
                elif len(found_dep) == 1:
                    self.install(found_dep[0], install_cmd, dry_cmd, packages=packages)
                else:
                    raise ValueError('Unable to install dependancy %s.' % dep)
        if 'prereq' in package.keys():
            for prereq in package['prereq']:
                Popen(prereq).wait()

        Popen([install_cmd if not self.h.dry_run else dry_cmd, package['name']]).wait()
        package['completed'] = True
        
        # in case it is a dependancy that wasn't listed as an independant package
        # (so reocurring dependancies aren't installed multiple times)
        return package

    def run(self, progress, interactive):
        if interactive:
            self.configure()

        for source in self.sources:
            print(source)
            data = self.h.parse_json(source)
            # use get if the parameter is non essential (because it doesn't raise a KeyError)
            manager = data.get('package_manager', '')
            prereq = data.get('prereq', '')
            install_cmd = data['install_cmd']
            dry_cmd = data.get('dry_run', '')
            packages = data['packages']

            Popen(prereq).wait()
            for pack in packages:
                pack['completed'] = False
                self.install(pack, install_cmd, dry_cmd, packages=packages)

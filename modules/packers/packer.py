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
        self.sources = [d for d in os.listdir(os.path.abspath(__file__).rsplit(os.sep, 1)[0]) if H.is_json(d)]

    def install(self, package, install_cmd, dry_cmd, packages=[]):
        if 'deps' in package.keys():
            for dep in package['deps']:
                found_dep = [p for p in packages if p['name'] == dep]
                if not found_dep:
                    self.install({ 'name': dep }, install_cmd, dry_cmd)
                elif len(found_dep) == 1 and not found_dep[0].get('completed'):
                    self.install(found_dep, install_cmd, dry_cmd, packages=packages)
                else:
                    raise ValueError('Unable to install dependancy %s.' % dep)
        if 'prereq' in package.keys():
            for prereq in package['prereq']:
                Popen(prereq).wait()

        Popen([all_cmd if not self.h.dry_run else dry_cmd, package['name']]).wait()
        package['completed'] = True

    def run(self, progress):
        for source in self.sources:
            data = self.h.parse_json(source)
            # use get if the parameter is non essential (because it doesn't raise a KeyError)
            manager = data.get('package_manager', '')
            install_cmd = data['install_cmd']
            dry_cmd = data.get('dry_run', '')
            packages = data['packages']

            for pack in packages:
                pack['completed'] = False
                self.install(pack, install_cmd, dry_cmd, packages=packages)
                

                # # execute common package installations
    # for pack in packages:
    #     v_logger(h.LOG_MODE.INFO, 'Parsing {} {}..'.format(pack, PACKAGE_EXTENSION.strip('.').upper()))
    #     package = h.parse_json(PACKAGE_DIR + pack + PACKAGE_EXTENSION)
    #     manager, install_cmd, fix_cmd, items, dry_cmd = (package['package_manager'],
    #                                                      package['install_cmd'],
    #                                                      package['fix_cmd'] if 'fix_cmd' in package.keys() else None,
    #                                                      package['packages'],
    #                                                      package['dry_run'] if 'dry_run' in file_dict.keys() else '')
    #     # execute prerequesites for package installs
    #     for item in items:
    #         if "prereq" in item.keys():
    #             v_logger(h.LOG_MODE.INFO, '{}: Executing prerequesites for {}..'.format(pack, item['name']))
    #             if DRY_RUN:
    #                 h.logger(h.LOG_MODE.CMD, ' && '.join(items['prereq']))
    #             else:
    #                 prereq_params = ' && '.join(item['prereq'])
    #                 if c_logger(Sn(stringify=lambda: prereq_params,
    #                                run=lambda: Popen(prereq_params).wait()), 0):
    #                     v_logger(h.LOG_MODE.ERR, '{}: Failed to execute prerequesites of {}'.format(pack, item['name']))
    #                     raise Exception('Failed to execute prerequesites of {} from package {}'.format(item['name'], pack))
    #         if "deps" in item.keys():
    #             v_logger(h.LOG_MODE.INFO, '{}: Installing dependencies for {}..'.format(pack, item['name']))
    #             deps_params = [install_cmd, dry_cmd if DRY_RUN else ''] + [dep for dep in item['deps']]
    #             if not c_logger(Sn(stringify=lambda: ' '.join(deps_params),
    #                            run=lambda: Popen(deps_params).wait()), 0):
    #                 v_logger(h.LOG_MODE.ERR, '{}: Failed to install dependencies for {}.'.format(pack, item['name']))
    #                 if not 'n' in input('Dependency installation failed, try to fix? [Y/n]: ').lower():
    #                     if not c_logger(stringify=lambda: fix_cmd,
    #                                     run=lambda: Popen(fix_cmd).wait(), 0):
    #                         raise Exception('Failed to fix dependencies of {}.'.format(item['name']))
    #                 else:
    #                     raise Exception('Failed to install dependencies of {}.'.format(item['name']))
    #     # execute final package installations
    #     v_logger(h.LOG_MODE.INFO, '{}: Installing all packages..'.format(pack))
    #     install_params = [install_cmd, dry_cmd if DRY_RUN else ''] + [item['name'] for item in items]
    #     if not c_logger(Sn(stringify=lambda: ' '.join(install_params),
    #                    run=lambda: Popen(install_params).wait()), 0):
    #         v_logger(h.LOG_MODE.ERR, '{}: Failed to install packages.'.format(pack))
    #         raise Exception('Failed to complete installation of {}.'.format(pack))


    # # load and run custom modules
    # for custom in customs:
    #     v_logger(h.LOG_MODE.INFO, 'Loading module {}'.format(custom))
    #     custom_mod = import_module(CUSTOM_DIR + custom)
    #     Custom = getattr(custom_mod, custom.title())
    #     c = Custom()
    #     v_logger(h.LOG_MODE.INFO, 'Running module {}'.format(custom))
    #     c.run()

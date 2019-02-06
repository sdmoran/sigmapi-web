import subprocess
import sys
import json
import os

PYTHON = 'python3.6'
PIP = 'sudo pip 3.6'
MANAGE = '{0} manage.py'.format(PYTHON)
DEV_DATA = 'fixtures/dev_data.json'

def r_requirements():
    print('r_requirements')
    subprocess.run('{0} install -r requirements/dev.txt'.split(' '))

def r_loaddata():
    print('r_loaddata')

def r_dumpdata():
    print('r_dumpdata')

def r_syncdb():
    print('r_syncdb')

def r_static():
    print('r_static')

def r_static_prod():
    print('r_static_prod')

def r_migrate():
    print('r_migrate')

def r_quickrun():
    print('r_quickrun')

def r_test():
    print('r_test')

def r_pycodestyle():
    print('r_pycodestyle')

def r_pylint():
    print('r_pylint')

def r_newmigrations():
    print('r_newmigrations')

def r_superuser():
    print('r_superuser')

def r_dbshell():
    print('r_dbshell')

def r_shell():
    print('r_shell')

def r_destroyenv():
    print('r_destroyenv')

def r_clean():
    print('r_clean')


commands = {
    'dev': ['requirements', 'loaddata', 'static'],
    'requirements': [r_requirements],
    'loaddata': ['syncdb', r_loaddata],
    'dumpdata': ['syncdb', r_dumpdata],
    'syncdb': [r_syncdb],
    'run': ['static', 'migrate', 'quickrun'],
    'static': [r_static],
    'static_prod': [r_static_prod],
    'migrate': [r_migrate],
    'quickrun': [r_quickrun],
    'test': [r_test],
    'quality': ['pycodestyle', 'pylint'],
    'pycodestyle': [r_pycodestyle],
    'pylint': [r_pylint],
    'newmigrations': [r_newmigrations],
    'superuser': [r_superuser],
    'dbshell': [r_dbshell],
    'shell': [r_shell],
    'destroyenv': ['clean', r_destroyenv],
    'clean': [r_clean]
}

def run_command(command, executed_functions):
    reqs = commands[command]
    for r in reqs:
        try:
            if r not in executed_functions:
                r()
                executed_functions.add(r)
        except TypeError:
            assert isinstance(r, str), 'Command list values must be callables or strings'
            run_command(r, executed_functions)


def run(command):
    run_command(command, set())


if __name__ == '__main__':
    run(sys.argv[1])

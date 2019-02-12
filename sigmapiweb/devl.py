""" 
devl.py -- The more cross-platform makefile substitute

Usage
=====
For first-time setup of this file, type 'python devl.py' 

How to Add Functionality
========================

User Variables
--------------
To add a new user variable, you should

- Update the ``user_variables`` dict in this module with the new key and a default value

This will make the variable available in calls to vformat() and format_and_call()

Commands
--------
To add a new command, you should

- Update the ``commands`` dict in this module
  - The key is the name of the command
  - The value is list containing other command names and/or functions which the command depends upon
- Prefix any new command functions with 'r_' (for 'run') for consistency
- Avoid pipes, redirects, or otherwise bash-y things for our Windows friends. Instead, just use multiple commands
  and rely on Python's baked-in io functionality. See r_dumpdata() and r_pylint() for examples.
"""

import subprocess
import sys
import json
import os
import glob

user_variables = {
    'PYTHON': 'python3.6',
    'PIP': 'sudo pip3.6',
    'MANAGE': 'python3.6 manage.py',
    'DEV_DATA': os.path.join('fixtures', 'dev_data.json'),
    'PORT': '8000',
}

help_commands_list = None  # Leave this empty, it is auto-populated

# Helper Functions

def vformat(space_separated):
    """ Format a string with global variables """
    return space_separated.format(**user_variables)

def format_and_call(space_separated, **kwargs):
    """ Format global variables within ``space_separated`` and then subprocess.run the string, separated by spaces.
    
    Passes ``kwargs`` to subprocess.run. Returns the output of subprocess.run. 
    Outputs the command executed similar to how make does it.
    Note this can be used even if there are no user_variable format specifiers.
    
    Arguments:
        space_separated (str): Space-separated command to run
        kwargs: (dict): Dict to pass to subprocess.run as **kwargs
    """
    cmdstr = vformat(space_separated)
    print(cmdstr)
    return subprocess.run(cmdstr.split(' '), **kwargs)

def just_call(complete_arguments, **kwargs):
    """ Same functionality as subprocess.run, but prints the command it is executing ahead of time.
    
    This function is different than format_and_call in that it doesn't attempt to substitute user_variables values
    and it takes a list of arguments, not a space-separated string. 

    Arguments:
        complete_arguments (list): First parameter of subprocess.run
        kwargs (dict): Passed as **kwargs to subprocess.run
    """
    print(' '.join(complete_arguments))
    return subprocess.run(complete_arguments, **kwargs)

def glob_as_args(glob_str, **kwargs):
    """ Outputs a file glob as a verbose space-separated argument string for maximum crossplatforminess.

        Arguments:
            glob_str (str): A valid glob string used as the first argument to glob.glob
            kwargs (dict): Keyword arguments to pass to glob.glob
    """
    return ' '.join(glob.glob(glob_str, **kwargs))

# Command Functions

def r_requirements():
    devreqs = os.path.join('requirements', 'dev.txt')
    format_and_call('{PIP} install -r ' + devreqs)

def r_loaddata():
    format_and_call('{MANAGE} loaddata {DEV_DATA}')

def r_dumpdata():
    complete = format_and_call(
        '{MANAGE} dumpdata --natural-foreign -e contenttypes -e auth.Permission', 
        stdout=subprocess.PIPE
    )
    with open(user_variables['DEV_DATA'], 'w') as f:
        f.write(complete.stdout.text)


def r_syncdb():
    format_and_call('{MANAGE}  migrate --run-syncdb')

def r_static():
    format_and_call('{MANAGE} collectstatic --noinput')

def r_static_prod():
    format_and_call('{MANAGE} compilecss')
    format_and_call('{MANAGE} collectstatic --noinput')

def r_migrate():
    format_and_call('{MANAGE} migrate')

def r_quickrun():
    format_and_call('{MANAGE} runserver 0.0.0.0:{PORT}')

def r_test():
    print('lol what tests')

def r_pycodestyle():
    format_and_call('pycodestyle common --max-line-length=120')
    apps_files = glob_as_args('apps/*')
    format_and_call("pycodestyle " + apps_files + " --exclude='apps/*/migrations/*' --max-line-length=120")
    scripts_path = os.path.abspath('../scripts')
    format_and_call('pycodestyle ' + scripts_path + ' --max-line-length=120')

def r_pylint():
    format_and_call('pylint common')
    apps_files = glob_as_args('apps/*')
    format_and_call('pylint ' + apps_files)
    scripts = os.path.abspath('../scripts') 
    format_and_call('pylint ' + scripts + ' --max_line_length=120')

def r_newmigrations():
    format_and_call('{MANAGE} makemigrations')
    print('Before you commit, remember to rename your migration with a description of what it does (but keep its numerical designator)')
    print('Example: Change "003_auto_20170101_1942.py" to something like "003_add_blacklist.py"')

def r_superuser():
    format_and_call('{MANAGE} createsuperuser')

def r_dbshell():
    format_and_call('{MANAGE} dbshell')

def r_shell():
    format_and_call('{MANAGE} shell')

def r_destroyenv():
    print('Destructive commands are not yet implemented')
    # TODO Destroy the entire python environment based on requirements.txt like the Makefile did?

def r_clean():
    print('Destructive commands are not yet implemented')

def r_help():
    print('devl.py -- The more cross-platform make-substitute for the Sigma Pi Gamma Iota website')
    print()
    print('Usage:')
    print('\t$ python devl.py COMMAND')
    print('Available commands are:')
    assert help_commands_list is not None, 'There was an issue populating the list of possible commands'
    for c in help_commands_list:
        print('\t' + c)


# Core Functionality

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
    'clean': [r_clean],
    'help': [r_help],
}

help_commands_list = sorted(list(commands.keys()))

def run_command(command, executed_functions):
    """ Runs the given named command or function.
    Functions are evaluated one time at maximum per call
    Arguments:
        command (str): The name of a command to run
        executed_functions (set): A set containing any command functions which have already been called
    """
    reqs = commands[command]
    for r in reqs:
        try:
            if r not in executed_functions:
                r()
                executed_functions.add(r)
        except TypeError:
            assert isinstance(r, str), 'Command list values must be callables or strings'
            run_command(r, executed_functions)
        except KeyboardInterrupt:
            pass


def run(command):
    """ Shortcut for first-time call of run_command() """
    run_command(command, set())


if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(sys.argv[1])
    else:
        print('Invalid argument format. Use "python devl.py help" for more information.')

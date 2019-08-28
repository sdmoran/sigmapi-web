""" 
devl.py -- The more cross-platform makefile substitute with setup tools

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
- Add a description of any new command functions using the `describe` decorator
- Avoid pipes, redirects, or otherwise bash-y things for our Windows friends. Instead, just use multiple commands
  and rely on Python's baked-in io functionality. See r_dumpdata() and r_pylint() for examples.
"""

import subprocess
import sys
import json
import os
import glob

# The values below are just defaults and will be superceded by devl_settings.json

user_variables = {
    'PYTHON': 'python3.6',
    'PIP': 'sudo pip3.6',
    'MANAGE': 'python3.6 manage.py',
    'DEV_DATA': os.path.join('fixtures', 'dev_data.json'),
    'PORT': '8000',
}

if os.name == 'nt':
    # We're in Windows, so we'll try different defaults
    user_variables.update({
        'PYTHON': 'python',
        'PIP': 'pip',
        'MANAGE': 'python manage.py'
    })

PROMPT = '\n{question}\n({options}) {default}\n> '
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


def prompt_user(question, options=('y', 'n'), case_sensitive=False, default_first=True, accept_any=False):
    """ Prompts the user with the given question, providing them with the given options
    Re-prompts the user until the response is in `options` unless accept_any=False
    If options not provided, defaults to y/n.
   Returns the user's input (in lowercase if case_sensitive=False)

    Arguments:
        question (str): The prompt for the user
        options (iter(str)): (optional) The tuple/iterable of possible options to answer
        case_sensitive (boolean): (optional) Whether or not the responses are case-sensitive
        default_first (boolean): (optional) Whether or not an empty input should default to the first option
        accept_any (boolean): Whether to check if the response is in the options. Automatically set to true if no options provided.
    """
    ops = ''
    if options:
        ops = '/'.join(options)
    elif accept_any:
        ops = 'any response accepted'
    assert ops != '', 'prompt_user(): No options are provided, but kwarg accept_any is false. This is probably an error.'
    default = ''
    if options and default_first:
        default = ' [{default}]'.format(default=options[0])
    prompt = PROMPT.format(question=question, options=ops, default=default)
    result = input(prompt)
    if default_first and result == '':
        result = options[0]
    valid_inputs = options if case_sensitive else [o.lower() for o in options]
    while (result if case_sensitive else result.lower()) not in valid_inputs and not accept_any:
        print('Invalid option.')
        result = input(prompt)
    return result if case_sensitive else result.lower()


def update_user_vars():
    """ Updates `user_vars` with the contents of devl_settings.json """
    with open('devl_settings.json', 'r') as settings_file:
        try:
            user_variables.update(json.load(settings_file))
        except json.decoder.JSONDecodeError as e:
            print('There is an error in your devl_setting.json file. Please fix it and try re-running your command.')
            print('The output is as follows:')
            print(e.msg)
            should_regen = prompt_user(
                'Would you like to just regenerate the file by running the setup script again?'
                '\nThe command you tried to execute will not run upon completion, so you have time to change the defaults.'
            )
            if should_regen == 'y':
                run('setup_devl')
            else:
                print('Okay, devl.py will now exit. Please fix the JSON file and try re-running the command.')
                exit(0)

def describe(description):
    """ Decorator used to add descriptions to command functions. Descriptions should be succinct and written in the imperative
    
    Arguments:
        description (str): A description of the actions the function takes
    """
    def wrapper(cmd_fn):
        cmd_fn._help_description_ = description
        return cmd_fn
    return wrapper

def description_of(cmd_str):
    """ Determines the description of the given command by chaining together descriptions of all functions it ends up calling 
    If a description cannot be found, uses the name of the function.
    
    Arguments:
        cmd_str (str): The name of the command to generate a description of
    """
    descs = [description_of(c) if isinstance(c, str) else '\t\t* ' + getattr(c, '_help_description_', c.__name__) for c in commands[cmd_str]]
    return '\n'.join(descs)

# Command Function Helpers

def download_pip():
    """ Tries to use get-pip.py to download pip """
    try:
        from urllib import request
        from urllib.error import URLError
    except ImportError:
        print('Unfortunately your python installation does not have urllib, so you will have to install pip manually.')
        print('I\'d reccomend googling "how to install pip on [YOUR PLATFORM]"')
        print('Once you have done so, re-run this script. You may have to restart your computer for the changes to take effect.')
        print('devl.py will now exit.')
        exit(0)
    try:
        get_pip = request.urlopen('https://bootstrap.pypa.io/get-pip.py').read()
    except URLError:
        print('There was an issue fetching get-pip.py. Are you connected to the internet?')
        print('If not, connect to the internet and re-run this script after doing so.')
        print('If you are connected yet this is not working, you will probably have to manually install pip.')
        print('I\'d reccomend googling "how to install pip on [YOUR PLATFORM]" if that is the case.')
        print('Once you have done so, re-run "python devl.py"')
        print('devl.py will now exit.')
        exit(0)
    with open('get-pip.py', 'wb') as gp_file:
        gp_file.write(get_pip)
    print('Successfully downloaded get_pip.py')

# Command Functions

@describe('Install all Python requirements using pip')

def r_requirements():
    devreqs = os.path.join('requirements', 'dev.txt')
    format_and_call('{PIP} install -r ' + devreqs)

    
@describe('Load fixture data to database')
def r_loaddata():
    format_and_call('{MANAGE} loaddata {DEV_DATA}')


@describe('Write current database as a fixture')
def r_dumpdata():
    complete = format_and_call(
        '{MANAGE} dumpdata --natural-foreign -e contenttypes -e auth.Permission',
        stdout=subprocess.PIPE
    )
    with open(user_variables['DEV_DATA'], 'w') as f:
        f.write(complete.stdout.text)


@describe('Migrate database with --run-syncdb')
def r_syncdb():
    format_and_call('{MANAGE}  migrate --run-syncdb')


@describe('Collect static files')
def r_static():
    format_and_call('{MANAGE} collectstatic --noinput')


@describe('Compile SASS files, then run collectstatic')
def r_static_prod():
    format_and_call('{MANAGE} compilescss')
    format_and_call('{MANAGE} collectstatic --noinput')

@describe('Migrate the database')
def r_migrate():
    format_and_call('{MANAGE} migrate')


@describe('Run the dev server')
def r_quickrun():
    format_and_call('{MANAGE} runserver 0.0.0.0:{PORT}')


@describe('Run tests (not implemented)')
def r_test():
    print('lol what tests')


@describe('Run the pycodestyle checks')
def r_pycodestyle():
    format_and_call('pycodestyle common --max-line-length=120')
    apps_files = glob_as_args('apps/*')
    format_and_call("pycodestyle " + apps_files +
                    " --exclude='apps/*/migrations/*' --max-line-length=120")
    scripts_path = os.path.abspath('../scripts')
    format_and_call('pycodestyle ' + scripts_path + ' --max-line-length=120')


@describe('Run the pylint checks')
def r_pylint():
    format_and_call('pylint common')
    apps_files = glob_as_args('apps/*')
    format_and_call('pylint ' + apps_files)
    scripts = os.path.abspath('../scripts')
    format_and_call('pylint ' + scripts + ' --max_line_length=120')


@describe('Create new migrations based on changes to Models')
def r_newmigrations():
    format_and_call('{MANAGE} makemigrations')
    print('Before you commit, remember to rename your migration with a description of what it does (but keep its numerical designator)')
    print('Example: Change "003_auto_20170101_1942.py" to something like "003_add_blacklist.py"')


@describe('Create a local admin account')
def r_superuser():
    format_and_call('{MANAGE} createsuperuser')


@describe('Open the database shell prompt')
def r_dbshell():
    format_and_call('{MANAGE} dbshell')


@describe('Start an interactive python session with convenience imports')
def r_shell():
    format_and_call('{MANAGE} shell')


@describe('Destroy the Python environment (not implemented)')
def r_destroyenv():
    print('Destructive commands are not yet implemented')
    # TODO Destroy the entire python environment based on requirements.txt like the Makefile did?

@describe('Clean static files (not implemented)')
def r_clean():
    print('Destructive commands are not yet implemented')


@describe('Display help text')
def r_help():
    print('devl.py -- The more cross-platform make-substitute for the Sigma Pi Gamma Iota website')
    print()
    print('Usage:')
    print('\t$ python devl.py COMMAND')
    print()
    print('Available commands are:')
    print()
    assert help_commands_list is not None, 'There was an issue populating the list of possible commands'
    for c in help_commands_list:
        print('\t' + c)
        print(description_of(c))
        print()


@describe('Run the environment setup script')
def r_setup_devl():
    working_settings = {}
    print('Welcome to devl.py -- The module that makes working with your dev environment suck a little less\n')
    print('This setup script can be re-accessed at any time after it is complete using "python devl.py setup_devl"')
    if not (sys.version_info > (3, 5)):
        print(
            'First things first, you need to install a newer version of python. '
            'Head over to python.org/downloads and get the latest version for your system.'
        )
        print('Once you have done so, add it to your system path and re-run this script using the new version')
        print('devl.py will now exit. See you soon!')
        exit(0)
    else:
        print('Congratulations on running this script with a compatible version of python!')
        working_settings['PYTHON'] = sys.executable
    if not os.path.isfile('devl_settings.json'):
        print('It has been detected that you have not yet set up devl.py. So let\'s do that!')
    print('Let\'s see if you have pip installed...')
    try:
        import pip
        print('Success!')
    except ModuleNotFoundError:
        print('It looks like this python installation does not have pip.')
        should_install = prompt_user(
            'Would you like devl.py to try to install pip for you?'
            ' You should not use this option if you installed this python interpereter using a package manager such as apt.'
            ' If you did, just answer "n" and then run "sudo apt install python3-pip" (Ubuntu) or whatever the equivalent on your system is.'
            ' That will allow your pip installation to be managed by your package manager.'
            ' If you are on Windows or Mac you should probably answer yes, unless you use a package manager such as choco or homebrew,'
            ' and that package manager has pip3 available.'
        )
        if(should_install == 'y'):
            download_pip()
            print('Installing pip...')
            if os.name == 'nt':
                format_and_call(working_settings['PYTHON'] + ' get-pip.py')
            else:
                format_and_call('sudo ' + working_settings['PYTHON'] + ' get-pip.py')
        else:
            print('Okay, please install pip for this interpreter and re-run devl.py once you have done so.')
            print('devl.py will now exit.')
            exit(0)
    if os.name == 'nt':
        working_settings['PIP'] = working_settings['PYTHON'] + ' -m pip'
    else:
        working_settings['PIP'] = 'sudo ' + working_settings['PYTHON'] + ' -m pip'
    working_settings['MANAGE'] = working_settings['PYTHON'] + ' manage.py'
    user_variables.update(working_settings)
    with open('devl_settings.json', 'w') as settings_file:
        settings_file.write(json.dumps(user_variables, indent=4))
    print('\%\%\%\% NOTICE \%\%\%\%')
    print('A file called devl_settings.json has been placed in this directory. It contains the default settings determined from this setup process.')
    print('If anything in devl.py doesn\'t work after this, you probably need to change something in that file.')
    print('Since you have the proper python toolchain installed, we can now set up the dev environment.')
    should_run_dev = prompt_user('Would you like to run `dev` now install your environment? (This can be done in the future using "python devl.py dev")')
    if os.name == 'nt':
        print('Since you are running Windows, you may need to install Visual Studio Dev Tools from https://visualstudio.microsoft.com/downloads/ in order to finish.')
        print('We\'ll go ahead and try running dev anyways. If it fails, go to the above link and install "Tools for Visual Studio".')
        print('Then, restart your computer, and then run "python devl.py dev"')
    if should_run_dev == 'y':
        run('dev')
    else:
        print('Setup is finished! Use "python devl.py dev" if you would like to install the environment in the future.')
        exit(0)
    print('Setup is finished! Check the output above to see if it succeeded.')
    print('Use "python devl.py help" to see what else devl.py can do.')
    print('devl.py will now exit.')
    exit(0)  # Explicit exit in case we're here due to malformed JSON


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
    'setup_devl': [r_setup_devl]
}

help_commands_list = sorted(list(commands.keys()))


def run_command(command, executed_functions):
    """ Runs the given named command or function.
    Functions are evaluated one time at maximum per call
    Arguments:
        command (str): The name of a command to run
        executed_functions (set): A set containing any command functions which have already been called
    """
    try:
        reqs = commands[command]
    except KeyError:
        sys.stderr.write('[devl.py] Invalid command "{0}"\n\n'.format(str(command)))
        raise
    for r in reqs:
        try:
            if r not in executed_functions:
                r()
                executed_functions.add(r)
        except TypeError:
            assert isinstance(
                r, str), 'Command list values must be callables or strings'
            run_command(r, executed_functions)
        except KeyboardInterrupt:
            pass


def run(command):
    """ Shortcut for first-time call of run_command() """
    run_command(command, set())


if __name__ == '__main__':
    if os.path.isfile('devl_settings.json'):
        update_user_vars()
        if len(sys.argv) == 2:
            run(sys.argv[1])
        else:
            sys.stderr.write('[devl.py] Invalid argument format. Use "python devl.py help" for more information.\n')
    else:
        if len(sys.argv) == 2:
            sys.stderr.write('[devl.py] Notice -- devl.py has not yet been set up. Using default user variables. To fix this, run `python devl.py` with no arguments.\n\n')
            run(sys.argv[1])
        else:
            run('setup_devl')


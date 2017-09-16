import subprocess
import os
import sys
import datetime
import argparse


def backup(db_user, db_name, file_name=None, compressed=False):
    """ Backs up the database ``db_name`` as ``user`` to ``file_name`` 
    
    If ``file_name`` not specified, stdout is used (to allow arbitrary redirection).
    If ``compressed`` is True, -Fc is used
    """
    cmd = ['pg_dump', '-U', db_user, db_name]
    if file_name:
        cmd += ['-f', file_name]
    if compressed:
        cmd += ['-Fc']
    subprocess.Popen(cmd)


def auto_name(db_name):
    """ Generates a unique name for the file based on today's date """
    g_name = '%s_dump_%s' % (db_name, datetime.datetime.now())
    i = 0
    while os.path.isfile(g_name):
        i += 1
    if i > 0:
        g_name = g_name + '%d' % i
    return g_name


def get_credentials(cmd_args):
    """ Returns (username, database_name) if they do not exist in args 
    
    Checks for environment variables if needed, prompts the user if any information is missing.
    """
    db_user = None
    db_name = None
    if not cmd_args.user:
        try:
            db_user = os.environ['POSTGRES_USER']
        except KeyError:
            sys.stderr.write(
                'No POSTGRES_USER environment variable is set. Either set the variable, or specify a user with -u.\n'
                'Also be sure POSTGRES_DB_NAME is set if not using -n flag.\n'
            )
            exit(-1)
    else:
        db_user = cmd_args.user
    if not cmd_args.name:
        try:
            db_name = os.environ['POSTGRES_DB_NAME']
        except KeyError:
            sys.stderr.write(
                'No POSTGRES_DB_NAME environment variable is set. Either set the variable, or specify a database with'
                ' -n.\nAlso be sure POSTGRES_USER is set if not using -u flag.\n'
            )
            exit(-1)
    else:
        db_name = cmd_args.user
    return db_user, db_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--user',
        help='The user under which the database is stored. '
             'Defaults to POSTGRES_USER environment variable'
    )
    parser.add_argument(
        '-n', '--name',
        help='The name of the database. '
             'Defaults to POSTGRES_DB_NAME environment variable'
    )
    parser.add_argument(
        '-c', '--compress',
        help='Flag indicating the backup should be compressed.'
    )
    args = parser.parse_args()
    user, name = get_credentials(args)
    if sys.stdout.isatty():
        f_name = auto_name(name)
    else:
        f_name = None
    if args.compress:
        compress = True
    else:
        compress = False
    backup(user, name, f_name, compress)

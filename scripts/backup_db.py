#!/usr/bin/python
"""
Script to back-up our Postgres database.
"""

import argparse
import datetime
import os
import subprocess
import sys

USER_ENVIRON = 'POSTGRES_USER'
NAME_ENVIRON = 'POSTGRES_DB_NAME'
PORT_ENVIRON = 'POSTGRES_PORT'


def main():
    """
    Parse command line arguments and possibly back up database.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--user',
        help='The user under which the database is stored. '
             'Defaults to %s environment variable' % USER_ENVIRON
    )
    parser.add_argument(
        '-n', '--name',
        help='The name of the database. '
             'Defaults to %s environment variable' % NAME_ENVIRON
    )
    parser.add_argument(
        '-p', '--port',
        help='The port through which the database can be accessed.'
             ' Defaults to %s environment variable' % PORT_ENVIRON
    )
    parser.add_argument(
        '-c', '--compress',
        help='Flag indicating the backup should be compressed.',
        action='store_true'
    )
    parser.add_argument(
        '-e', '--environment',
        help='Flag indicating that the proper environment variables:\n'
             '%s, %s, %s\n'
             'should be set to the values used during this run.' % (NAME_ENVIRON, USER_ENVIRON, PORT_ENVIRON),
        action='store_true'
    )
    args = parser.parse_args()
    user, name, port = get_credentials(args)
    if sys.stdout.isatty():
        f_name = auto_name(name)
    else:
        f_name = None
    if args.compress:
        compress = True
    else:
        compress = False
    if args.environment:
        set_environment_vars(name, user, port)
    backup(user, name, port, f_name, compress)


def backup(db_user, db_name, db_port, file_name=None, compressed=False):
    """
    Backs up the database.

    Arguments:
        db_user (str): Username to use to backup database.
        db_name (str): Database name.
        db_port (str): Database port.
        file_name (str): Output file. Defaults to STDOUT.
        compressed (bool): If True, -Fc is used
    """
    cmd = ['pg_dump', '-U', db_user, db_name, '-p', db_port]
    if file_name:
        cmd += ['-f', file_name]
    if compressed:
        cmd += ['-Fc']
    subprocess.Popen(cmd)


def auto_name(db_name):
    """
    Generates a unique name for the file based on today's date.

    Arguments:
        db_name (str)

    Returns: str
    """
    g_name = '%s_dump_%s' % (db_name, datetime.datetime.now())
    if os.path.isfile(g_name):
        i = 1
        while os.path.isfile(g_name + '(%d)' % i):
            i += 1
        g_name = g_name + '(%d)' % i
    return g_name


def get_credentials(cmd_args):
    """
    Returns (username, database name, database port) if they do not exist in args.

    Checks for environment variables if needed, prompts the user if any
    information is missing.

    Arguments:
        cmd_args (parsed arguments)

    Returns: (str, str)
    """
    db_user = None
    db_name = None
    db_port = None
    if not cmd_args.user:
        try:
            db_user = os.environ[USER_ENVIRON]
        except KeyError:
            sys.stderr.write(
                'No %s environment variable is set.'
                'Either set the variable, or specify a user with -u.\n'
                'Also be sure %s is set if not using -n flag and %s is set if not using -p flag.\n'
                % (USER_ENVIRON, NAME_ENVIRON, PORT_ENVIRON)
            )
            exit(-1)
    else:
        db_user = cmd_args.user
    if not cmd_args.name:
        try:
            db_name = os.environ[NAME_ENVIRON]
        except KeyError:
            sys.stderr.write(
                'No %s environment variable is set.'
                'Either set the variable, or specify a database with'
                ' -n.\nAlso be sure %s is set if not using '
                '-u flag and %s is set if not using -p flag.\n'
                % (NAME_ENVIRON, USER_ENVIRON, PORT_ENVIRON)
            )
            exit(-1)
    else:
        db_name = cmd_args.name
    if not cmd_args.port:
        try:
            db_port = os.environ[PORT_ENVIRON]
        except KeyError:
            sys.stderr.write(
                'No %s environment variable is set. Either set the variable, or specify a database with'
                ' -n.\nAlso be sure %s is set if not using -u flag and %s is set if not using -n flag.\n'
                % (PORT_ENVIRON, USER_ENVIRON, NAME_ENVIRON)
            )
            exit(-1)
    else:
        db_port = cmd_args.port
    return db_user, db_name, db_port


def set_environment_vars(db_name, db_user, db_port):
    """ Sets the environment variables to the """
    os.environ[NAME_ENVIRON] = db_name
    os.environ[USER_ENVIRON] = db_user
    os.environ[PORT_ENVIRON] = db_port


if __name__ == '__main__':
    main()

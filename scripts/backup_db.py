#!/usr/bin/python
"""
Script to back-up our Postgres database.
"""

import argparse
import datetime
import os
import subprocess
import sys


def main():
    """
    Parse command line arguments and possibly back up database.
    """
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
    f_name = auto_name(name) if sys.stdout.isatty() else None
    backup(user, name, f_name, args.compress)


def backup(db_user, db_name, file_name=None, compressed=False):
    """
    Backs up the database.

    Arguments:
        db_name (str): Database name.
        user (str): Username to use to backup database.
        file_name (str): Output file. Defaults to STDOUT.
        compressed (bool): If True, -Fc is used
    """
    cmd = ['pg_dump', '-U', db_user, db_name]
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
    Returns (username, database_name) if they do not exist in args.

    Checks for environment variables if needed, prompts the user if any
    information is missing.

    Arguments:
        cmd_args (parsed arguments)

    Returns: (str, str)
    """
    db_user = None
    db_name = None
    if not cmd_args.user:
        try:
            db_user = os.environ['POSTGRES_USER']
        except KeyError:
            sys.stderr.write(
                'No POSTGRES_USER environment variable is set.' +
                'Either set the variable, or specify a user with -u.\n' +
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
                'No POSTGRES_DB_NAME environment variable is set.' +
                'Either set the variable, or specify a database with' +
                ' -n.\nAlso be sure POSTGRES_USER is set if not using ' +
                '-u flag.\n'
            )
            exit(-1)
    else:
        db_name = cmd_args.user
    return db_user, db_name


if __name__ == '__main__':
    main()

# These settings must be DIFFERENT depending on whether the site is running
# in development, or in production.

# This file contains the DEVELOPMENT version of each of those settings.
# When the site is deployed in production, this file is COMPLETELY overwritten
# by a copy which resides on the server. That copy must STAY on the server,
# because it contains sensitive data that should not be commited in our public
# repository.

# If you need to make modifications to this file at any point, you will also
# need to make changes to the version on the server, before deploying.
import os
BASE_DIR = os.getcwd()

DEBUG = True

ADMINS = (
    ('Development', 'test@doesntmatter.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'database',                      # Or path to database file if using sqlite3.

        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

DOWNLOADVIEW_BACKEND = 'django_downloadview.lighttpd.XSendfileMiddleware'

# Todo: These should probably be absolute paths in prod.
MEDIA_ROOT = './content/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = './static_dir'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR,'static'),
)

FILE_UPLOAD_TEMP_DIR = BASE_DIR

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bg#3p7$1l7i=^frmpvx!##nzsbt-eg$cy!(1-a#m9k(l0rksw7'

# In dev no emails are sent.
EMAIL_HOST = None
EMAIL_PORT = None
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
DEFAULT_FROM_EMAIL = None
SERVER_EMAIL = None

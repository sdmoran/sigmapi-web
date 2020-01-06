"""
Development settings for Sigma Pi, Gamma Iota chapter website.
"""
import os

# pylint: disable=unused-wildcard-import
from .base import *  # pylint: disable=wildcard-import


DEBUG = True

ADMINS = (
    ('Development', 'test@doesntmatter.com'),
)

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database',   # Or path to database file if using sqlite3.

        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',    # Empty for localhost through domain sockets
                       # or '127.0.0.1' for localhost through TCP.
        'PORT': '',    # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

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
    os.path.join(BASE_DIR, 'static'),
)

# Describe to django where to find fixtures
# useful for loading fixture data during testing
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

FILE_UPLOAD_TEMP_DIR = BASE_DIR

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bg#3p7$1l7i=^frmpvx!##nzsbt-eg$cy!(1-a#m9k(l0rksw7'

# In dev no emails are sent.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = None
EMAIL_PORT = None
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
DEFAULT_FROM_EMAIL = None
SERVER_EMAIL = None

# Override other email constants
EC_EMAIL = "gr-sigmapi@local.dev"
ACTIVES_EMAIL = "sigmapiactives@local.dev"
ALUMNI_EMAIL = "sigmapialumni@local.dev"

# Placeholders for slack integrations
SIGMA_POLLS_SLACK_CLIENT_SECRET = b'NotARealSecret'

CLIQUE_SLACK_SIGNING_SECRET = b'AlsoAfakeSecret'
CLIQUE_SLACK_OATH_TOKEN = b'YepThatsOAuth2'

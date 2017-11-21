"""
Base settings for Sigma Pi, Gamma Iota chapter website.
"""

import os


BASE_DIR = os.getcwd()

EC_EMAIL = "sigmapi@wpi.edu"
ACTIVES_EMAIL = "sigmapiactives@wpi.edu"
ALUMNI_EMAIL = "sigmapialumni@wpi.edu"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/content/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'sass_processor.finders.CssFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/secure/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
            ],
        },
    }
]

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DOWNLOADVIEW_RULES = [
    {
        'destination_dir': 'lightpd-optimized-by-middleware',
    },
]

ROOT_URLCONF = 'common.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'common.wsgi.application'

PREREQ_APPS = (
    'django',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'sass_processor',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)
PROJECT_APPS = (
    'common',
    'apps.PubSite',
    'apps.UserInfo',
    'apps.Archive',
    'apps.PartyList',
    'apps.Secure',
    'apps.Links',
    'apps.Standards',
    'apps.Scholarship',
)
INSTALLED_APPS = PREREQ_APPS + PROJECT_APPS

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SASS_PROCESSOR_AUTO_INCLUDE = False
SASS_PRECISION = 8

PUBLIC_PAGES = {
    'Home': ('pub-index', None),
    'About': ('pub-about', 'summer-house.jpg'),
    'Service & Activities': ('pub-activities', 'volleyball.jpg'),
    'Brothers':  ('userinfo-users', 'seniors-2017.jpg'),
    'Log In': ('pub-login', None),  # This image is hard-coded into login_v1.scss
}

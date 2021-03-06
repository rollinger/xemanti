# Django settings for xemanti project.

import os
import sys
import manage
import instance_settings

DEBUG = instance_settings.DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Phil', 'philipp.rollinger@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xemanti',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'xemanti-sudo',
        'PASSWORD': 'comMahakalaxemanti.',
        'HOST': 'localhost',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
    }
}

#if 'test' in sys.argv:
#    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['127.0.0.1','85.214.123.105','.xemanti.com','.xemanti.net','h2170983.stratoserver.net']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de-de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

SITE_ROOT = os.path.dirname(os.path.realpath(manage.__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = "/source/xemanti_static/"

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(BASE_DIR, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
    #'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'zinnia.context_processors.version', # Optional
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Disabled - activate maybee later...
    #'xemanti.middleware.AnonymousSpamProtectionMiddleware',
    'xemanti.middleware.CrawlerBlockerMiddleware',
    'xemanti.middleware.AnonymousRatingMiddleware',
)

ROOT_URLCONF = 'xemanti.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'xemanti.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'xemanti/templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.admindocs',
    # Django Packages
    'south',
    'djcelery',
    #'kombu.transport.django',
    'dajaxice',
    'dajax',
    'tagging',
    'mptt',
    'zinnia',
    'chart_tools',
    #'compress',
    # Installed Apps
    'xemanti',
    'usr_profile',
    'ngramengine',
    'rating',
    'reporting',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

from xemanti.logging_filters import skip_suspicious_operations

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        # Define filter
        'skip_suspicious_operations': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_suspicious_operations,
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', 'skip_suspicious_operations'],
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

#
# Django Celery Configuration
#
# Start Worker with:
# ./manage.py celery worker --loglevel=info -B
# ./manage.py celeryd -v 2 -B -s celery -E -l INFO 
import djcelery
djcelery.setup_loader()
# Using RabbitMQ 
BROKER_URL = 'amqp://guest:guest@localhost:5672/'

#BROKER_HOST = "localhost"
#BROKER_PORT = 5672
#BROKER_USER = "xemanti-sudo"
#BROKER_PASSWORD = "comMahakalaxemanti."
#BROKER_VHOST = "localhost"
#BROKER_URL = "amqp://xemanti-sudo@localhost:5672/localhost"
# List of modules to import when celery starts.
#CELERY_IMPORTS = ("ngramengine.tasks", )


#BROKER_URL = "amqp://guest:guest@localhost:5672//"
#CELERY_RESULT_BACKEND = "amqp"
#CELERY_TASK_RESULT_EXPIRES = 18000
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYBEAT_LOADER = "djcelery.loaders.DjangoLoader"

"""
XEMANTI CONFIGURATION SETTINGS
"""
REGISTRATION_START_BALANCE = 100.00
ANONYMOUS_RATING_CYCLES = 3

"""
Spam Protection Configuration
- probability each request of showing captcha
- urls where Spam Protection is enabled
Alternatively:
if the context variable open_captcha is set to 'true' the subsequent template will show the modal dialog
"""
SPAM_PROTECTED_PROBABILITY = 0.02
SPAM_PROTECTED_URLS = ['/rating/','/reporting/']

SPAM_PROTECTED_URL_PROBABILITY = {'/rating/': 0.02, '/reporting/': 0.02}

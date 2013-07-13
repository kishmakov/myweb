import os.path

# Django settings for common project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# absolute path uniquely settled
PROJECT_LOCATION = os.path.join(os.path.dirname(__file__), '..')
# SITE_URL = 'http://localhost:8000'
SITE_URL = 'http://192.168.1.6:8000'

def make_full(relative_path):
    return os.path.join(PROJECT_LOCATION, relative_path).replace('\\','/')


ADMINS = (
    ('Kirill Shmakov', 'shmakir@yandex.ru'),
)

MANAGERS = ADMINS

# bases

DATABASE_ROUTERS = ['vle.routers.VleRouter']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': make_full('bases/system.db')
    },

    'fluids': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': make_full('bases/vle/fluids.db')
    }
}

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'en-US'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# prefixes

ADMIN_MEDIA_PREFIX = '/static/admin/'

# paths

MEDIA_ROOT = ''
STATIC_ROOT = make_full('static')

# urls

MEDIA_URL = ''
# STATIC_URL = SITE_URL + '/static/'
STATIC_URL = SITE_URL + '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u9$7_9b=dk$5uhlv@d-t55alr#5xl#usvp)go!5-)53n7f836c34543,g'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSOR = ("django.contrib.auth.context_processors.auth",
 "django.core.context_processors.debug",
 "django.core.context_processors.i18n",
 "django.core.context_processors.media",
 "django.core.context_processors.static",
 "django.core.context_processors.tz",
 "django.contrib.messages.context_processors.messages")


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'common.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'common.wsgi.application'

TEMPLATE_DIRS = (
    make_full('templates'),
    make_full('templates/vle'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'vle',
)

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

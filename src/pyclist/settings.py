"""
Django settings for pyclist project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
import logging
import os
import warnings
from datetime import datetime

import pycountry
import sentry_sdk
from django.contrib.gis.geoip2 import GeoIP2
from django.core.paginator import UnorderedObjectListWarning
from django.utils.translation import gettext_lazy as _
from environ import Env
from pytz import utc
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from stringcolor import cs

from pyclist import conf

# disable UnorderedObjectListWarning when using autocomplete_fields
warnings.filterwarnings('ignore', category=UnorderedObjectListWarning)

# Build paths inside the project like this: path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED_DIR = os.path.join(BASE_DIR, 'sharedfiles')

env = Env()
env.read_env(env('DJANGO_ENV_FILE'))
env.read_env(env('DJANGO_DB_CONF', default='/run/secrets/db_conf'))
env.read_env(env('DJANGO_SENTRY_CONF', default='/run/secrets/sentry_conf'))

ADMINS = conf.ADMINS

MANAGERS = ADMINS

EMAIL_HOST = conf.EMAIL_HOST
EMAIL_HOST_USER = conf.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = conf.EMAIL_HOST_PASSWORD
EMAIL_PORT = conf.EMAIL_PORT
EMAIL_USE_TLS = conf.EMAIL_USE_TLS

SERVER_EMAIL = 'Clist <%s>' % EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = 'Clist <%s>' % EMAIL_HOST_USER

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = conf.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!

DEV_ENV = 'dev'
PROD_ENV = 'prod'
ENVIRONMENT = env('DJANGO_ENV')
PYLINT_ENV = ENVIRONMENT == 'pylint'
DEBUG = ENVIRONMENT == DEV_ENV or PYLINT_ENV

# Application definition

INSTALLED_APPS = (
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'clist',
    'ranking',
    'tastypie',
    'my_oauth',
    'true_coders',
    'jsonify',  # https://pypi.python.org/pypi/django-jsonify/0.2.1
    'tastypie_swagger',
    'tg',
    'notification',
    'crispy_forms',
    'crispy_bootstrap3',
    'events',
    'django_countries',
    'el_pagination',
    'django_static_fontawesome',
    'django_extensions',
    'django_user_agents',
    'django_json_widget',
    'django_ltree',
    'webpush',
    'oauth2_provider',
    'channels',
    'chats',
    'favorites',
    'guardian',
    'django_rq',
    'notes',
    'logify',
    'fontawesomefree',
    'corsheaders',
    'submissions',
    'modeltranslation',
    'donation',
    'silk',
)

MIDDLEWARE = (
    'pyclist.middleware.CompressionMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django_brotli.middleware.BrotliMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'pyclist.middleware.SetUpCSRFToken',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'csp.middleware.CSPMiddleware',
    'pyclist.middleware.UpdateCoderLastActivity',
    'pyclist.middleware.CustomRequestMiddleware',
    'pyclist.middleware.RequestIsAjaxFunction',
    'pyclist.middleware.RedirectMiddleware',
    'pyclist.middleware.SetAsCoder',
    'pyclist.middleware.Lightrope',
    'pyclist.middleware.StatementTimeoutMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

if DEBUG:
    DEBUG_PERMISSION_EXCLUDE_PATHS = {'static'}
    MIDDLEWARE += (
        'pyclist.middleware.DebugPermissionOnlyMiddleware',
        'django_cprofile_middleware.middleware.ProfilerMiddleware',
    )
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


ROOT_URLCONF = 'pyclist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'pyclist.context_processors.global_settings',
                'pyclist.context_processors.coder_time_info',
                'pyclist.context_processors.fullscreen',
                'pyclist.context_processors.favorite_settings',
            ],
            'builtins': [
                'pyclist.templatetags.staticfiles',
                'clist.templatetags.extras',
                'django.contrib.humanize.templatetags.humanize',
                'favorites.templatetags.favorites_extras',
                'django.templatetags.cache',
                'el_pagination.templatetags.el_pagination_tags',
                'jsonify.templatetags.jsonify',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'string_if_invalid': '',
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'pyclist.wsgi.application'

ASGI_APPLICATION = 'pyclist.asgi.application'

CHANNEL_LAYERS_CAPACITY = 10_000

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
            'capacity': CHANNEL_LAYERS_CAPACITY,
        },
    },
}


# Subdomain settings
SESSION_COOKIE_DOMAIN = ".clist.by"
SESSION_COOKIE_SECURE = True


# django_rq
RQ_QUEUES = {
    'system': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DEFAULT_TIMEOUT': 120,  # 2 minutes
    },
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DEFAULT_TIMEOUT': 1800,  # 30 minutes
    },
    'parse_statistics': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DEFAULT_TIMEOUT': 86400,  # 24 hours
    },
    'parse_accounts': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DEFAULT_TIMEOUT': 21600,  # 6 hours
    },
}
RQ_SHOW_ADMIN_LINK = True


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASES_ = {'postgresql': {'ENGINE': 'django.db.backends.postgresql_psycopg2'}}
if not PYLINT_ENV:
    DATABASES_['postgresql'].update({
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    })

DATABASES = {
    'default': DATABASES_['postgresql'],
}
DATABASES.update(DATABASES_)


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'IGNORE_EXCEPTIONS': True,
        }
    }
}


USER_AGENTS_CACHE = 'default'


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
REPO_STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_JSON_TIMEZONES = os.path.join(BASE_DIR, 'static', 'json', 'timezones.json')
RESOURCES_ICONS_PATHDIR = 'img/resources/'
RESOURCES_ICONS_SIZES = [32, 64]

STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'static_compress.CompressedStaticFilesStorage'},
}

STATIC_COMPRESS_METHODS = ['gz']


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_SIZES_PATHDIR = 'sizes/'

TASTYPIE_DEFAULT_FORMATS = ['json', 'jsonp', 'yaml', 'xml', 'plist']

HIGHLIGHT_STYLES_FOLDER = os.path.join(REPO_STATIC_ROOT, 'highlight/styles')
HIGHLIGHT_STYLE_SUFFIX = '.min.css'
HIGHLIGHT_STYLES = []
for style in os.listdir(HIGHLIGHT_STYLES_FOLDER):
    if style.endswith(HIGHLIGHT_STYLE_SUFFIX):
        HIGHLIGHT_STYLES.append(style[:-len(HIGHLIGHT_STYLE_SUFFIX)])
HIGHLIGHT_STYLES.sort()

LOGIN_URL = '/login/'

APPEND_SLASH = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': PYLINT_ENV,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'db': {
            'format': str(cs('[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s', 'grey')),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console_debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'console_info': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'db': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'db',
        },
        'development': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'dev.log'),
            'formatter': 'verbose',
            'delay': True,
        },
        'production': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'prod.log'),
            'formatter': 'verbose',
            'delay': True,
        },
        'debug': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'debug.log'),
            'formatter': 'verbose',
            'delay': True,
        },
        'telegrambot': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'telegram.log'),
            'formatter': 'verbose',
            'delay': True,
        },
    },
    'loggers': {
        **{
            k: {
                'handlers': ['null'],
                'propagate': False,
            }
            for k in (
                'django.security.DisallowedHost',
                'parso.python.diff',
                'PIL',
                'googleapiclient.discovery',
                'daphne',
                'asyncio',
                'numba.core',
            )
        },
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
        },
        'telegrambot': {
            'handlers': ['telegrambot'],
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['db'],
            'level': env('DJANGO_DB_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        '': {
            'handlers': ['console_debug', 'console_info', 'development', 'production', 'debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


TELEGRAM_TOKEN = env('TELEGRAM_TOKEN', default=conf.TELEGRAM_TOKEN)
TELEGRAM_NAME = env('TELEGRAM_NAME', default=conf.TELEGRAM_NAME)
TELEGRAM_ADMIN_CHAT_ID = conf.TELEGRAM_ADMIN_CHAT_ID

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap3'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

COUNTRIES_OVERRIDE = {
    'CZ': {'names': ['Czech Republic', 'Czechia', 'Чехия']},
    'MK': {'names': ['Macedonia', 'North Macedonia', 'Македония']},
    'PS': {'names': ['Palestine', 'Palestine, State of', 'Палестина']},
    'KP': {'names': ['North Korea', 'Democratic People\'s Republic of Korea', 'Korea, Democratic People\'s Republic of', 'КНДР', 'Северная Корея']},  # noqa
    'KR': {'names': ['South Korea', 'Republic of Korea', 'Южная Корея', 'Korea, Republic of', 'Korea']},
    'MO': {'names': ['Macao', 'Macau', 'Макао', 'Macao, China']},
    'US': {'names': ['United States of America', 'United States', 'America', 'Virgin Islands', 'UM', 'United States Minor Outlying Islands', 'Соединенные Штаты Америки', 'США']},  # noqa
    'VN': {'names': ['Vietnam', 'Viet Nam', 'Вьетнам']},
    'GB': {'names': ['United Kingdom', 'United Kingdom of Great Britain', 'England', 'UK', 'Scotland', 'Northern Ireland', 'Wales', 'Великобритания', 'Англия', 'Шотландия']},  # noqa
    'MD': {'names': ['Moldova', 'Молдова', 'Молдавия', 'Republic of Moldova', 'Moldova, Republic of']},
    'KG': {'names': ['Kyrgyzstan', 'Кыргызстан', 'Киргизия']},
    'RS': {'names': ['Serbia', 'Srbija', 'Сербия']},
    'HR': {'names': ['Croatia', 'Hrvatska', 'Хорватия']},
    'CN': {'names': ['China', '中国', 'Китай']},
    'PL': {'names': ['Poland', 'Republic of Poland', 'Польша']},
    'RU': {'names': ['Russia', 'Россия', 'Russian Federation', 'Российская Федерация']},
    'SU': {'names': ['Soviet Union', 'Советский Союз']},
    'TR': {'names': ['Turkey', 'Türkiye', 'Турция']},
    'IR': {'names': ['Iran', 'Islamic Republic of Iran', 'Iran, Islamic Republic of', 'Иран']},
    'SY': {'names': ['Syria', 'Syrian Arab Republic', 'Сирия']},
    'BO': {'names': ['Bolivia', 'Plurinational State of Bolivia', 'Bolivia, Plurinational State of', 'Боливия']},
    'TW': {'names': ['Taiwan', 'Taiwan, Province of China', 'Тайвань']},
    'HK': {'names': ['Hong Kong', 'Hong Kong, China', 'Гонконг']},
}
DISABLED_COUNTRIES = {'UM'}


ALPHA2_FIXES_MAPPING = {
    'AIDJ': 'A0',
    'BQAQ': 'B0',
    'BYAA': 'B1',
    'GEHH': 'G0',
    'SKIN': 'S0',
    'CSXX': 'Y0',
}

HISTORICAL_COUNTRIES = set()
for country in pycountry.historic_countries:
    code = ALPHA2_FIXES_MAPPING.pop(country.alpha_4, country.alpha_2)
    assert not pycountry.countries.get(alpha_2=code)

    override = COUNTRIES_OVERRIDE.setdefault(code, {})
    assert not override.get('alpha3')
    names = [name.strip() for name in country.name.split(',')]
    assert names
    if names[-1].endswith(' of'):
        assert len(names) > 1
        names[-1] += ' ' + names[0]
    names = [name for name in names if not pycountry.countries.get(name=name)]

    override.setdefault('names', []).extend(names)
    if not pycountry.countries.get(alpha_3=country.alpha_3):
        override.setdefault('alpha3', country.alpha_3)
    if hasattr(country, 'numeric'):
        override.setdefault('numeric', country.numeric)
    HISTORICAL_COUNTRIES.add(code)

CUSTOM_COUNTRIES_ = getattr(conf, 'CUSTOM_COUNTRIES', {})
FILTER_CUSTOM_COUNTRIES_ = getattr(conf, 'FILTER_CUSTOM_COUNTRIES', {})


# guardian
ANONYMOUS_USER_NAME = None
GUARDIAN_AUTO_PREFETCH = True


# DJANGO DEBUG TOOLBAR
if DEBUG:
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'pyclist.middleware.NonHtmlDebugToolbarMiddleware',
    )
    INSTALLED_APPS += ('debug_toolbar',)

    DEBUG_TOOLBAR_DISABLE_PANELS = {
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.request.RequestPanel',
    }

    DEBUG_TOOLBAR_PANELS = [
        panel for panel in [
          'debug_toolbar.panels.history.HistoryPanel',
          'debug_toolbar.panels.versions.VersionsPanel',
          'debug_toolbar.panels.timer.TimerPanel',
          'debug_toolbar.panels.settings.SettingsPanel',
          'debug_toolbar.panels.headers.HeadersPanel',
          'debug_toolbar.panels.sql.SQLPanel',
          'debug_toolbar.panels.staticfiles.StaticFilesPanel',
          'debug_toolbar.panels.cache.CachePanel',
          'debug_toolbar.panels.signals.SignalsPanel',
          'debug_toolbar.panels.profiling.ProfilingPanel',
          'debug_toolbar.panels.templates.TemplatesPanel',
          'debug_toolbar.panels.redirects.RedirectsPanel',
          'debug_toolbar.panels.request.RequestPanel',
        ]
        if panel not in DEBUG_TOOLBAR_DISABLE_PANELS
    ]

    def show_toolbar_callback(request):
        first_path = request.path.split('/')[1]
        return (
            first_path not in DEBUG_PERMISSION_EXCLUDE_PATHS and
            not request.is_ajax() and
            'disable_dtb' not in request.GET and
            (not DEBUG or request.user.is_authenticated)
        )

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar_callback,
        'DISABLE_PANELS': DEBUG_TOOLBAR_DISABLE_PANELS,
    }


# DJANGO SILK
if DEBUG:
    MIDDLEWARE += (
        'silk.middleware.SilkyMiddleware',
    )
    SILKY_PYTHON_PROFILER = True
    SILKY_AUTHENTICATION = True
    SILKY_AUTHORISATION = True
    SILKY_META = True

    def SILKY_PERMISSIONS(user):
        return user.is_authenticated and user.is_superuser


# WEBPUSH
WEBPUSH_SETTINGS = conf.WEBPUSH_SETTINGS

# OAUTH2 PROVIDER
OAUTH2_PROVIDER = {
    'DEFAULT_SCOPES': ['read'],
}


CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = 15768000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_URLS_REGEX = '^/api/.*$'

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https:", "data:")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'")
CSP_IMG_SRC = CSP_DEFAULT_SRC
CSP_CONNECT_SRC = CSP_DEFAULT_SRC

# CSP Yandex counter
CSP_SCRIPT_SRC += ('https://mc.yandex.ru', 'https://yastatic.net', )
CSP_IMG_SRC += ('https://mc.yandex.ru', )
CSP_CONNECT_SRC += ('https://mc.yandex.ru', )

# CSP Google counter
CSP_SCRIPT_SRC += ('https://www.google-analytics.com', 'https://www.googletagmanager.com', )
CSP_IMG_SRC += ('https://www.google-analytics.com', )
CSP_CONNECT_SRC += ('https://www.google-analytics.com', )

# CSP Yandex form
CSP_SCRIPT_SRC += ('https://forms.yandex.ru', )

# X-XSS-Protection
SECURE_BROWSER_XSS_FILTER = True


# MODELTRANSLATION
MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ru', )
LOCALE_CHOICES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)
LOCALE_DEFAULT = MODELTRANSLATION_DEFAULT_LANGUAGE


# CONSTANTS
VIEWMODE_ = 'list'
OPEN_NEW_TAB_ = False
ADD_TO_CALENDAR_ = 'enable'
COUNT_PAST_ = 3
GROUP_LIST_ = True
HIDE_CONTEST_ = False
FAVORITE_SETTINGS_ = {
    'contests': True,
    'problems': True,
}
DEFAULT_TIME_ZONE_ = 'UTC'
CHANING_HOSTS_ = ['clist.by', 'dev.clist.by']
ALLOWED_REDIRECT_HOSTS_ = {'clist.by', 'dev.clist.by', 'grafana.clist.by'}
HOST_ = 'dev.clist.by' if DEBUG else 'clist.by'
HTTPS_HOST_URL_ = 'https://' + HOST_
MAIN_HOST_URL_ = 'https://clist.by'
CLIST_RESOURCE_DICT_ = {
    'host': HOST_,
    'pk': 0,
    'icon': 'img/favicon/favicon-32x32.png',
    'kind': 'global_rating',
    'colors': [],
}
EMAIL_PREFIX_SUBJECT_ = '[Clist] '
STOP_EMAIL_ = getattr(conf, 'STOP_EMAIL', False)
TIME_FORMAT_ = '%d.%m %a %H:%M'
LIMIT_N_TOKENS_VIEW = 3
LIMIT_TOKENS_VIEW_WAIT_IN_HOURS = 24
YES_ = {'', '1', 'yes', 'y', 'true', 't', 'on'}
NONE_ = {'null', 'none'}
ACE_CALENDARS_ = {
    'enable': {'id': 'enable', 'name': 'Enable'},
    'disable': {'id': 'disable', 'name': 'Disable'},
    'google': {'id': 1, 'name': 'Google'},
    'yahoo': {'id': 2, 'name': 'Yahoo'},
    'outlook': {'id': 3, 'name': 'Outlook'},
}
PAST_CALENDAR_ACTIONS_ = ['show', 'lighten', 'darken', 'lighten-day', 'darken-day', 'hide']
PAST_CALENDAR_DEFAULT_ACTION_ = 'lighten'
ORDERED_MEDALS_ = ['gold', 'silver', 'bronze']
THEMES_ = ['default', 'cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', 'lumen', 'paper', 'readable',
           'sandstone', 'simplex', 'slate', 'spacelab', 'superhero', 'united', 'yeti']
SESSION_DURATIONS_ = {
    '1 day': {'value': 60 * 60 * 24},
    '1 week': {'value': 60 * 60 * 24 * 7},
    '1 month': {'value': 60 * 60 * 24 * 30, 'default': True},
    '1 year': {'value': 60 * 60 * 24 * 365},
    '1 life': {'value': datetime.max.replace(tzinfo=utc)},

}

DEFAULT_COUNT_QUERY_ = 10
DEFAULT_COUNT_LIMIT_ = 100

ADDITION_HIDE_FIELDS_ = {'problems', 'solved', 'hack', 'challenges', 'url'}
INSIVIBLE_CONTEST_KIND = 'hidden'
STAGE_CONTEST_KIND = 'stage'
PROBLEM_STATISTIC_FIELDS = (
    # problem_field, statistic_field, contest_field
    ('language', '_languages', 'languages'),
    ('verdict', '_verdicts', 'verdicts'),
)
PROBLEM_IGNORE_KINDS = {INSIVIBLE_CONTEST_KIND, STAGE_CONTEST_KIND}
PROBLEM_API_IGNORE_FIELDS = {'solution', 'external_solution', 'user_solution'}
PROBLEM_USER_SOLUTION_SIZE_LIMIT = 65536

VIRTUAL_CODER_PREFIX_ = '∨'

DEFAULT_API_THROTTLE_AT_ = 10

CODER_LIST_N_VALUES_LIMIT_ = 100
CODER_N_SUBSCRIPTIONS_LIMIT_ = 10
CODER_SUBSCRIPTION_N_LIMIT_ = CODER_LIST_N_VALUES_LIMIT_
CODER_SUBSCRIPTION_TOP_N_LIMIT_ = 50

ENABLE_GLOBAL_RATING_ = False
CHART_N_BINS_LIMIT = 300
CHART_N_BINS_DEFAULT = 40


FONTAWESOME_ICONS_ = {
    'institution': '<i class="fa-fw fas fa-university"></i>',
    'country': '<i class="fa-fw fab fa-font-awesome-flag"></i>',
    'room': '<i class="fa-fw fas fa-door-open"></i>',
    'affiliation': '<i class="fa-fw fas fa-user-friends"></i>',
    'city': '<i class="fa-fw fas fa-city"></i>',
    'school': '<i class="fa-fw fas fa-school"></i>',
    'class': '<i class="fa-fw fas fa-user-graduate"></i>',
    'job': '<i class="fa-fw fas fa-building"></i>',
    'rating': '<i class="fa-fw fas fa-chart-line"></i>',
    'medal': '<i class="fa-fw fas fa-medal"></i>',
    'region': '<i class="fa-fw fas fa-map-signs"></i>',
    'location': '<i class="fa-fw fa-solid fa-location-dot"></i>',
    'chat': '<i class="fa-fw fas fa-user-friends"></i>',
    'advanced': '<i class="fa-fw far fa-check-circle"></i>',
    'n_advanced': '<i class="fa-fw far fa-check-circle"></i>',
    'company': '<i class="fa-fw fas fa-building"></i>',
    'language': '<i class="fa-fw fas fa-code"></i>',
    'languages': '<i class="fa-fw fas fa-code"></i>',
    'verdicts': '<i class="fa-fw fas fa-scroll"></i>',
    'league': '<i class="fa-fw fas fa-chess"></i>',
    'degree': '<i class="fa-fw fas fa-user-graduate"></i>',
    'university': '<i class="fa-fw fas fa-university"></i>',
    'list': '<i class="fa-fw fas fa-list"></i>',
    'group': '<i class="fa-fw fas fa-user-friends"></i>',
    'group_ex': '<i class="fa-fw fas fa-user-friends"></i>',
    'college': '<i class="fa-fw fas fa-university"></i>',
    'resource': '<i class="fa-fw fas fa-at"></i>',
    'field': '<i class="fa-fw fas fa-database"></i>',
    'database': '<i class="fa-fw fas fa-database"></i>',
    'admin': '<i class="fa-solid fa-screwdriver-wrench"></i>',
    'find_me': '<i class="fa-fw fas fa-crosshairs"></i>',
    'search': '<i class="fa-fw fas fa-search"></i>',
    'detail_info': '<i class="fa-fw fas fa-info"></i>',
    'solution_info': '<i class="fa-fw fa-regular fa-file-code"></i>',
    'short_info': '<i class="fa-fw fas fa-times"></i>',
    'score_in_row': '<i class="fa-fw fas fa-balance-scale"></i>',
    'luck': '<i class="fa-fw fas fa-dice"></i>',
    'tag': '<i class="fa-fw fas fa-tag"></i>',
    'hide': '<i class="fa-fw far fa-eye-slash"></i>',
    'show': '<i class="fa-fw far fa-eye"></i>',
    'delete': '<i class="fa-fw far fa-trash-alt"></i>',
    'period': '<i class="fa-fw far fa-clock"></i>',
    'date': '<i class="fa-fw far fa-calendar-alt"></i>',
    'n_participations': {'icon': '<i class="fa-fw fas fa-running"></i>', 'title': 'Number of participations'},
    'chart': '<i class="fa-fw fas fa-chart-bar"></i>',
    'ghost': '<i class="fa-fw fs-fw fas fa-ghost"></i>',
    'top': '<i class="fa-fw fas fa-list-ol"></i>',
    'coders': '<i class="fa-fw fas fa-users"></i>',
    'coder_kind': '<i class="fa-fw fas fa-user-tag"></i>',
    'accounts': '<i class="fa-fw fa-regular fa-rectangle-list"></i>',
    'problems': '<i class="fa-fw fa-solid fa-list-check"></i>',
    'participants': '<i class="fa-fw fas fa-users"></i>',
    'submissions': '<i class="fa-fw fa-solid fa-bars"></i>',
    'finalists': '<i class="fa-solid fa-user-group"></i>',
    'versus': '<i class="fa-fw fas fa-people-arrows"></i>',
    'last_activity': '<i class="fa-fw far fa-clock"></i>',
    'fullscreen': '<i class="fa-fw fas fa-expand-arrows-alt"></i>',
    'update': '<i class="fa-fw fas fa-sync"></i>',
    'vertical-expand': '<i class="fa-solid fa-arrows-up-down"></i>',
    'vertical-collapse': '<i class="fa-solid fa-xmark"></i>',
    'left-arrow': '<i class="fa-solid fa-angle-left"></i>',
    'right-arrow': '<i class="fa-solid fa-angle-right"></i>',
    'open_in_tab': '<i class="fa-fw fas fa-external-link-alt"></i>',
    'extra_url': '<i class="fa-fw fas fa-external-link-alt"></i>',
    'copy': '<i class="fa-fw far fa-copy"></i>',
    'copied': '<i class="fa-fw fas fa-copy"></i>',
    'pin': '<i class="fa-fw far fa-star"></i>',
    'unpin': '<i class="fa-fw fas fa-star"></i>',
    'timeline': '<i class="fa-fw fas fa-history"></i>',
    'contest': '<i class="fa-fw fas fa-laptop-code"></i>',
    'kofi': {'icon': '<i class="fa-fw fas fa-mug-hot ko-fi"></i>', 'title': None},
    'crypto': {'icon': '<i class="fa-fw fab fa-bitcoin"></i>', 'title': None},
    'fav': {'icon': '<i class="fa-fw fas fa-star activity fav selected-activity"></i>', 'title': 'Favorite',
            'name': 'fa-star', 'unselected_class': 'far', 'check_field': 'is_favorite'},
    'unfav': {'icon': '<i class="fa-fw far fa-star activity fav"></i>', 'title': None},
    'sol': {'icon': '<i class="fa-fw fas fa-check activity sol"></i>', 'name': 'fa-check', 'check_field': 'is_solved'},
    'rej': {'icon': '<i class="fa-fw fas fa-times activity rej"></i>', 'name': 'fa-times', 'check_field': 'is_reject'},
    'tdo': {'icon': '<i class="fa-fw fas fa-calendar-day activity tdo"></i>', 'name': 'fa-calendar-day',
            'check_field': 'is_todo'},
    'allsolved': {'icon': '<i class="fa-fw far fa-check-circle sol"></i>', 'name': 'fa-check-circle',
                  'selected_class': 'far', 'unselected_class': 'far'},
    'allreject': {'icon': '<i class="fa-fw far fa-times-circle rej"></i>', 'name': 'fa-times-circle',
                  'selected_class': 'far', 'unselected_class': 'far'},
    'status': '<i class="fa-fw far fa-lightbulb"></i>',
    'n_participants': {'icon': '<i class="fa-fw fas fa-users"></i>', 'title': 'Number of participants',
                       'position': 'bottom'},
    'participation': '<i class="fa-fw fas fa-user-check"></i>',
    'n_problems': {'icon': '<i class="fa-fw fa-solid fa-list-check"></i>', 'title': 'Number of problems',
                   'position': 'bottom'},
    'series': '<i class="fa-fw fas fa-trophy"></i>',
    'app': '<i class="fa-fw fas fa-desktop"></i>',
    'sort': '<i class="fa-fw fa-solid fa-sort"></i>',
    'sort_column': '<i class="fa-fw fa-solid fa-sort"></i>',
    'sort-asc': '<i class="fa-fw fas fa-sort-amount-down-alt"></i>',
    'sort-desc': '<i class="fa-fw fas fa-sort-amount-down"></i>',
    'verification': '<i class="fa-fw far fa-check-circle"></i>',
    'verified': '<i class="fa-fw verified fas fa-check-circle"></i>',
    'unverified': '<i class="fa-fw unverified fas fa-check-circle"></i>',
    'ips': '<i class="fa-fw fas fa-user-secret"></i>',
    'secret': '<i class="fa-fw fas fa-user-secret"></i>',
    'log': '<i class="fa-fw fas fa-scroll" style="--fa-animation-duration: 2s;"></i>',
    'on': '<i class="fa-fw fas fa-toggle-on"></i>',
    'off': '<i class="fa-fw fas fa-toggle-off"></i>',
    'more': '<i class="fa-fw fas fa-ellipsis-h"></i>',
    'note': {'icon': '<i class="fa-fw far fa-edit"></i>', 'name': 'fa-edit', 'check_field': 'is_note',
             'selected_class': 'far note-edit', 'unselected_class': 'far note-edit'},
    'badge': {'icon': '<i class="fa-fw fas fa-tag"></i>'},
    'virtual': '<i class="fa-fw fas fa-globe"></i>',
    'private': '<span class="fa-fw label label-success"><i class="fa-fw fa-solid fa-lock"></i></span>',
    'restricted': '<span class="fa-fw label label-warning"><i class="fa-fw fa-solid fa-unlock"></i></span>',
    'public': '<span class="fa-fw label label-danger"><i class="fa-fw fa-solid fa-lock-open"></i></span>',
    'as_coder': '<i class="fa-fw fa-solid fa-user-group"></i>',
    'logify': '<i class="fa-fw fa-regular fa-file-lines"></i>',
    'is_virtual': {'icon': '<i class="fa-fw fa-solid fa-clock-rotate-left"></i>', 'title': False},
    'to_list': {'icon': '<i class="fa-fw fa-solid fa-list-check"></i>', 'title': 'Add to list'},
    'invert': '<i class="fa-fw fa-solid fa-rotate"></i>',
    'stage': '<i class="fa-fw fa-regular fa-object-group"></i>',
    'fulltable': {'icon': '<i class="fa-fw fa-solid fa-up-down"></i>', 'title': 'Load full table'},
    'charts': '<i class="fa-fw fa-solid fa-chart-line"></i>',
    'dev': '<i class="fa-fw fa-regular fa-clone"></i>',
    'medal_scores': '<i class="fa-fw fas fa-chart-line"></i>',
    'merged_standings': '<i class="fa-fw fa-solid fa-object-group"></i>',
    'finish': '<i class="fa-fw fa-solid fa-flag-checkered"></i>',
    'virtual_start': '<i class="fa-fw fa-solid fa-stopwatch"></i>',
    'unfreezing': '<i class="fa-fw fa-regular fa-snowflake"></i>',
    'exclamation': '<i class="fa-fw fa-solid fa-circle-exclamation"></i>',
    'close': '<i class="fa-fw fa-solid fa-xmark"></i>',
    'locked': '<i class="fa-fw fa-solid fa-lock"></i>',
    'rating-change-up': {'icon': '<i class="fa-fw fas fa-angle-up"></i>', 'title': False},
    'rating-change-down': {'icon': '<i class="fa-fw fas fa-angle-down"></i>', 'title': False},
    'rating-change-same': {'icon': '<i class="fa-fw fa-solid fa-equals fa-2xs"></i>', 'title': False},
    'loading': '<i class="fa-fw fas fa-circle-notch fa-spin"></i>',
    'profile': {'icon': '<i class="fa-fw fa-regular fa-address-card"></i>', 'title': False},
    'rating_prediction': '<i class="fa-fw fa-solid fa-calculator"></i>',
    'https': '<i class="fa-fw fa-regular fa-square-check"></i>',
    'http': '<i class="fa-fw fa-regular fa-rectangle-xmark"></i>',
    'add': '<i class="fa-fw fas fa-plus"></i>',
    'edit': '<i class="fa-fw fa-regular fa-pen-to-square"></i>',
    'login': '<i class="fa-fw fa-solid fa-right-to-bracket"></i>',
    'logout': '<i class="fa-fw fa-solid fa-right-from-bracket"></i>',
    'expires': '<i class="fa-fw fa-solid fa-clock-rotate-left"></i>',
    'subscription': '<i class="fa-fw fa-regular fa-newspaper"></i>',
    'field_instead_key': '<i class="fa-fw fa-solid fa-pencil"></i>',
    'active_executions': {
        'icon': '<i class="text-muted fa-solid fa-gear fa-spin fa-lg" style="--fa-animation-duration: 5s;"></i>',
        'title': 'Updating…',
    },
    'google': {'icon': '<i class="fa-fw fab fa-google"></i>', 'title': None},
    'facebook': {'icon': '<i class="fa-fw fab fa-facebook"></i>', 'title': None},
    'youtube': {'icon': '<i class="fa-fw fab fa-youtube"></i>', 'title': None},
    'twitch': {'icon': '<i class="fa-fw fab fa-twitch"></i>', 'title': None},
    'github': {'icon': '<i class="fa-fw fab fa-github"></i>', 'title': None},
    'yandex': {'icon': '<i class="fa-fw fab fa-yandex-international"></i>', 'title': None},
    'discord': {'icon': '<i class="fa-fw fab fa-discord"></i>', 'title': None},
    'vk': {'icon': '<i class="fa-fw fab fa-vk"></i>', 'title': None},
    'patreon': {'icon': '<i class="fa-fw fab fa-patreon"></i>', 'title': None},
    'yandex-contest': {'icon': '<i class="fa-fw fas fa-tools"></i>'},
    'n_gold': '<span class="trophy trophy-detail gold-trophy"><i class="fas fa-trophy"></i></span>',
    'n_silver': '<span class="trophy trophy-detail silver-trophy"><i class="fas fa-trophy"></i></span>',
    'n_bronze': '<span class="trophy trophy-detail bronze-trophy"><i class="fas fa-trophy"></i></span>',
    'sum': '&sum;',
    'matching': '<i class="fa-solid fa-magnifying-glass"></i>',
    'silk': '<i class="fa-solid fa-magnifying-glass-chart"></i>',
}


STANDINGS_FIELDS_ = {
    'n_gold_problems': '<span class="trophy trophy-detail gold-trophy"><i class="fas fa-trophy"></i></span>',
    'n_silver_problems': '<span class="trophy trophy-detail silver-trophy"><i class="fas fa-trophy"></i></span>',
    'n_bronze_problems': '<span class="trophy trophy-detail bronze-trophy"><i class="fas fa-trophy"></i></span>',
}

STANDINGS_WITH_DETAIL_DEFAULT = True
STANDINGS_WITH_SOLUTION_DEFAULT = False
STANDINGS_WITH_AUTORELOAD_DEFAULT = True
STANDINGS_SMALL_N_STATISTICS = 1000
STANDINGS_FREEZE_DURATION_FACTOR_DEFAULT = 0.2
STANDINGS_UNSPECIFIED_PLACE = '-'
STANDINGS_STATISTIC_FIELDS = ['upsolving', 'total_solving', 'n_solved', 'n_upsolved', 'n_total_solved', 'n_first_ac']

ACCOUNT_STATISTIC_FIELDS = ['solving', 'upsolving', 'total_solving', 'n_solved', 'n_upsolved', 'n_total_solved',
                            'n_first_ac', 'n_gold', 'n_silver', 'n_bronze', 'n_medals',
                            'n_first_places', 'n_second_places', 'n_third_places', 'n_top_ten_places', 'n_places']

UPSOLVING_FILTER_DEFAULT = True

GEOIP_PATH = os.path.join(SHARED_DIR, 'GeoLite2-Country.mmdb')
GEOIP_ACCOUNT_ID = getattr(conf, 'GEOIP_ACCOUNT_ID')
GEOIP_LICENSE_KEY = getattr(conf, 'GEOIP_LICENSE_KEY')

GEOIP = None
if os.path.exists(GEOIP_PATH):
    GEOIP = GeoIP2(GEOIP_PATH)
elif GEOIP_ACCOUNT_ID or GEOIP_LICENSE_KEY:
    logging.warning('GeoIP database not found. Run ./manage.py download_geoip_database to download it.')

FILTER_FIELD_SUFFIX = '_field'


class NOTIFICATION_CONF:
    EMAIL = 'email'
    TELEGRAM = 'telegram'
    WEBBROWSER = 'webbrowser'

    METHODS_CHOICES = (
        (TELEGRAM, 'Telegram'),
        (WEBBROWSER, 'WebBrowser'),
        # (EMAIL, 'Email'),
    )


SHELL_PLUS_IMPORTS = [
    ('django.core.management', 'call_command'),
    ('collections', 'defaultdict'),
    ('tqdm'),
]


# Sentry
if not DEBUG:
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
        ],
        traces_sample_rate=0.005,
        profiles_sample_rate=0.005,
        send_default_pii=True,
        environment='development' if DEBUG else 'production',
    )

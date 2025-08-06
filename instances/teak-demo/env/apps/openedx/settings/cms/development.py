# -*- coding: utf-8 -*-
import os
from cms.envs.devstack import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "connect": False,
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Meilisearch connection parameters
MEILISEARCH_ENABLED = True
MEILISEARCH_URL = "http://meilisearch:7700"
MEILISEARCH_PUBLIC_URL = "http://meilisearch.www.myopenedx.com"
MEILISEARCH_INDEX_PREFIX = "tutor_"
MEILISEARCH_API_KEY = "6ff8ec4f48a8d3b6e52f5ca9e5b015bd20765c8a4c575eda0ae9493a5f979be5"
MEILISEARCH_MASTER_KEY = "ZVYegk6MBr4SHqwDKfXPq9g2"
SEARCH_ENGINE = "search.meilisearch.MeilisearchEngine"

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 604800, # 1 week
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "ora2-storage": {
        "KEY_PREFIX": "ora2-storage",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    }
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "My Open edX - http://www.myopenedx.com"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings

# REMOVE-AFTER-V20: check if we can remove these lines after upgrade.
from django.utils.deprecation import RemovedInDjango50Warning, RemovedInDjango51Warning
# RemovedInDjango5xWarning: 'xxx' is deprecated. Use 'yyy' in 'zzz' instead.
warnings.filterwarnings("ignore", category=RemovedInDjango50Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango51Warning)
# DeprecationWarning: 'imghdr' is deprecated and slated for removal in Python 3.13
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pgpy.constants")

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "http://www.myopenedx.com/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "7PFGSyjNZhnR4mlKCJpgkyB9"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "FsFKL7S37qhmAbEA8sghOMd08t4e0L40BL2jDW-BLWMhTS13860SaFuG39yFjgh2NB03p8T1mNAztCzZquBUtk7r0A77v77Mhv6fADELVfLglwsspIt1F_Ae-WasaB7N2Xe3daaNqIa4_vOjUJ9JGbEnO7GR9RIaEdrLH-238Z28KFcOfDHiDXMceYn6XJa3gwv47thWWt5oG0JhDXLa8XQPY9AfV6ygOfEINaqYWLmM5la4Xu24Sq1DqvGbNXKOdwaDLQYZO-cOOzONuY5gO-_2T9CSU5i1V5fQzYOAMMDYrKqjFf3_t4zYEkW2-QEb-QFevCcoireZWguWk5I7MQ",
        "n": "wFN-WV56RIzuToslskByIW8N4IntV4YiCW5UfQOV_Axe1HIBfY7CtHWCQgKwHxnTYedt11h1uYn0ZB7UvbSUZDjbL_bhpmovmeOKbTdAen5Vgb31jtO_ZvtGowR71VF7Bg97Uu9Ff-ndMPMRHEfl4lxXUfhlHR8Sa8pIl16eDg-HU1w494B5B1tWPF75Oq8eUfDI2SnOYlWgANGuCxM2xWQQhUzY75hvdEYH7kI-No-hS2QihxddmgO9HiUMv_xCqMQXuiE_jgfSr4LlPOmjMHEmu6msiibY6Ate50QAYQMHBlCbQpSsNE14dVb3zrBqiQbIdK_E2_0VidrETGh25w",
        "p": "0vshFCvH6MAuEmRqRNC2EP3cMMETxZkOIq1dI0NYnMEcJV83VtqaxpJ9IyFVu5IV5z8j3bydNx-aMdfC7eiYlWgshvMe6CeO9misoXW1bq8OE_B2kiQfgH6u07R2ONz2-oJcu7RBf378gavu06pJIBS0SdDJsGHlMQ_QoBBvdr0",
        "q": "6V1XYKTiBcSpiWsOhqLbAUCvPPHxz12wxqF8uDb-RRdlidL3wZwn_Q1SwqPCpYds7eKqF5JZKSwdZkqASpWyY0_g_BeXGXa0vuJ6Ud88VXG7Nz_6ccBS_Dke_YTvh9qlD2_WCSJlNebBKYb8vA3zTyOFzxS_j7Geylck_tKgoHM",
        "dq": "au1vFQRX4Ea9XA7myAAlE0zdPrKplteaIVlrOUlRdr0CtIUrKtZvaD7Llg3NKWWFHvcF8ukG25uwGOe4IvS2mVTHhRsWC__dT72cSJleHtSO8QDqs2ZpX9KYhZd83aXsjcczrlnJQEpsZafJdC18N93R-RHLuH6tgI8vj2dZXEs",
        "dp": "EdaDvHXbKBWfj5SH25ud2R_tjv20Ez_Wjx4DQuj9w_sbyxkaz7AZ5_IYvHCkFADM80lGWggJbtCwM8ifRYgl5nPxV9OUaGJ31uOQvPH7zgjk8tCg5chCFZYgZ-vZFwOvqgx9lK0v4Hy3EqubvK-oERtPBvKtKsmMHDLPG8ln8y0",
        "qi": "cSOV7lBJY5gIW-xLWyuZuaiv4oqDvrqdX7Oel3mExTqmfBQ3DGgZ0_pzWLPCmPfwRbcuW-FcyB0_exn2QvxHKKi4-mV4FM0AA7PN1wIaP80cTNcD_ceZDCkC5R9uvH93pOg84sJQwiXKyZi9bBFOcLgO2brM5vst1EYVhiHRFA0",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "wFN-WV56RIzuToslskByIW8N4IntV4YiCW5UfQOV_Axe1HIBfY7CtHWCQgKwHxnTYedt11h1uYn0ZB7UvbSUZDjbL_bhpmovmeOKbTdAen5Vgb31jtO_ZvtGowR71VF7Bg97Uu9Ff-ndMPMRHEfl4lxXUfhlHR8Sa8pIl16eDg-HU1w494B5B1tWPF75Oq8eUfDI2SnOYlWgANGuCxM2xWQQhUzY75hvdEYH7kI-No-hS2QihxddmgO9HiUMv_xCqMQXuiE_jgfSr4LlPOmjMHEmu6msiibY6Ate50QAYQMHBlCbQpSsNE14dVb3zrBqiQbIdK_E2_0VidrETGh25w",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://www.myopenedx.com/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "7PFGSyjNZhnR4mlKCJpgkyB9"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = True
# Note: CORS_ALLOW_HEADERS is intentionally not defined here, because it should
# be consistent across deployments, and is therefore set in edx-platform.

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

OPENEDX_LEARNING = {
    'MEDIA': {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": "/openedx/media-private/openedx-learning",
        }
    }
}

# Forum configuration
FORUM_SEARCH_BACKEND = "forum.search.meilisearch.MeilisearchBackend"
FEATURES["ENABLE_DISCUSSION_SERVICE"] = True
# Forum mongodb configuration, for existing platforms still running mongodb
FORUM_MONGODB_DATABASE = "cs_comments_service"
FORUM_MONGODB_CLIENT_PARAMETERS = {
    "host": "mongodb",
    "port": 27017,
    
    
    "ssl": False,
}
{}


FORUM_MONGODB_CLIENT_PARAMETERS["authSource"] = "admin"


import re
import logging

logger = logging.getLogger(__file__)

SENTRY_IGNORED_ERRORS = []

def validate_exc(method, value, exc_value, exc_class_name):
    if method == 'exc_class':
        # exc_class_name = value
        return exc_class_name == value

    elif method == 'exc_text':
        exc_text_expr = value
        for expr in exc_text_expr:
            if re.search(expr, exc_value):
                return True

        return False


def should_ignore_by_rule(rule, exc_value, exc_class_name):
    """
    Validates if a given ignored exception rule matches the current exception
    """
    for method, value in rule.items():
        result = validate_exc(method, value, exc_value, exc_class_name)
        if not result:
            return False
    return True

def exception_filter_hook(event, hint):
    """
    Calls the proper method to verify which exceptions are ignored
    for sentry
    """
    exc_text = ''
    exc_value = None

    if 'log_record' in hint:
        exc_text = hint['log_record'].message
    if 'exc_info' in hint:
        _exc_type, exc_value, _tb = hint['exc_info']
        exc_class_name = _exc_type.__name__
        exc_text += str(exc_value)

    for rule in SENTRY_IGNORED_ERRORS:
        ignore_event = should_ignore_by_rule(rule, exc_text, exc_class_name)
        if ignore_event:
            return None

    return event

try:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn="",
        integrations=[
            DjangoIntegration(),
        ],
        before_send=exception_filter_hook,
        send_default_pii=True,
        **{'traces_sample_rate': 0.0, 'profiles_sample_rate': 0.0},
    )
except ImportError:
    logger.error("Sentry SDK is not installed.")
# SCORM SETTINGS
def scorm_xblock_storage(xblock):
    from django.conf import settings
    from storages.backends.s3boto3 import S3Boto3Storage
    from xmodule.util.xmodule_django import get_current_request_hostname

    domain = get_current_request_hostname()

    if not domain:
        if SERVICE_VARIANT == "lms":
            domain = settings.LMS_BASE
        else:
            domain = settings.CMS_BASE

    return S3Boto3Storage(
        bucket_name=AWS_STORAGE_BUCKET_NAME,
        access_key=AWS_ACCESS_KEY_ID,
        secret_key=AWS_SECRET_ACCESS_KEY,
        querystring_expire=86400,
        custom_domain=f"{domain}/scorm-proxy"
    )
XBLOCK_SETTINGS["ScormXBlock"] = {
    "STORAGE_FUNC": scorm_xblock_storage,
}


LOGGING["loggers"].pop("tracking")
LOGGING["loggers"][""]["handlers"] = ["console"]

FORUM_MONGODB_DATABASE = "cs_comments_service"
######## End of settings common to LMS and CMS

######## Common CMS settings
STUDIO_NAME = "My Open edX - Studio"

CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_cms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_cms",
}

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "oaJOK6Fv4Sq62EzyGozpIq1u"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False  # scheme is correctly included in redirect_uri
SESSION_COOKIE_NAME = "studio_session_id"

MAX_ASSET_UPLOAD_FILE_SIZE_IN_MB = 100

FRONTEND_LOGIN_URL = LMS_ROOT_URL + '/login'
FRONTEND_REGISTER_URL = LMS_ROOT_URL + '/register'

# Enable "reindex" button
FEATURES["ENABLE_COURSEWARE_INDEX"] = True

# Create folders if necessary
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)



######## End of common CMS settings

LMS_BASE = "www.myopenedx.com:8000"
LMS_ROOT_URL = "http://" + LMS_BASE

CMS_BASE = "studio.www.myopenedx.com:8001"
CMS_ROOT_URL = "http://" + CMS_BASE

MEILISEARCH_PUBLIC_URL = "http://meilisearch.www.myopenedx.com:7700"

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso-dev"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = LMS_ROOT_URL

FEATURES["PREVIEW_LMS_BASE"] = "preview.www.myopenedx.com:8000"

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

ENABLE_COMPREHENSIVE_THEMING = True
COMPREHENSIVE_THEME_DIRS.extend(['/openedx/themes/ednx-saas-themes/edx-platform', '/openedx/themes/ednx-saas-themes/edx-platform/bragi-children'])
# MFE-specific settings

COURSE_AUTHORING_MICROFRONTEND_URL = "http://apps.www.myopenedx.com:2001/authoring"
CORS_ORIGIN_WHITELIST.append("http://apps.www.myopenedx.com:2001")
LOGIN_REDIRECT_WHITELIST.append("apps.www.myopenedx.com:2001")
CSRF_TRUSTED_ORIGINS.append("http://apps.www.myopenedx.com:2001")

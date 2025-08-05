# -*- coding: utf-8 -*-
import os
from cms.envs.production import *

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
MEILISEARCH_API_KEY = "af0bb89be027c1e35962accde72bf158f3c4d6bed8158e48dda262f6035f0d4b"
MEILISEARCH_MASTER_KEY = "OWGGkvUclXbWTQMqbWpMQf9j"
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
JWT_AUTH["JWT_SECRET_KEY"] = "JwTlRUcLIWFm9Uz9K9NinH3I"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "Pzz_ODc-zE2TXxJ5PVcJ5zgnevSrtVlUDKe8xr1E-UCMxxfEZWyXnuQxnPq-riNDkoIYDqeizqaFei4SNOmbJRwuwYoShao5WlS-8IOyzYLjb8AZ9LsQqMlRb6nRQ3ykHJLdv2ixpF4rbx-TNOdohAdLbxzOBjPkk1EzLyr3UTE986DyOZ9YD0YAXNHzic1Jq_feLZw-B0Sqp6C1Rkcq4HvbxOoSKLbWM71KmyeUIUoiEgDCmuzxo02RY9sz2eif1l_F8kg95tv4wtZKmnMn_zvF3LvRY0LTS6rjbLdvTZz0isGQLO-6k7cueA_0oXrQtEjeKanX_U61sCM9EWHVYQ",
        "n": "qB45SzWy292aXNtod3d_YS3i31o_qFLXerOgR7dYwHZdCrj237wtz7BrA73-A-y-eJpMr_Pi0oeKXv5CaLdEZm0elwqiaWPjopoz-jZIiczAbrHNH9QxDhob7ILFnF6esEcN8F2OEluhmNmvNpEbk1WFh2AhmBdfkjuiIKE8UK3qrOnwplKn6McPk4vDPdVel5utYaYDI33t0sBGn5J4XF0MrpPEFS2MH-eeRgTlAgAM-x3bpZbk6XAtlNvoiX2GWa0hCDIgBq3AfoHyFxmqicXOV-UT13ETOd3gDLEgfBDgXxviZ8m5pkXOq5Rc0XLvsbBHb1hvnLLVrgGWpTjnew",
        "p": "wNUHBpsCmb4i00XGj9gZAXOcf0mREYZ2zhO3oGfViPXWs9b9Fs-A1-uf6d2FkIsDCS0x5hmvRO69oAiMs0SC0jP74yj8Wtr7hfO8nymzul9tXoFNBc21918qgdgH5hL57npFedCOp0eHQiC52Ckez7jWSc_Y4YOr5QXwqH-gzOc",
        "q": "3zCqPKMTuXFmuKPQPwfZ0eQ4OzRtYeVxRpTWa5OIazrBs9gmqGzAciG3wB4JyMNFQadDBFZd4NwCTJFJr8EMjAgfBhs1xK57B0E3ahkT_9eP66iNW4Qu7q0m780ePbkBp6sJOIvu7_DQ4t3dANeFkwAv_a4JXJfQs5t4blPLyk0",
        "dq": "dli4vESAzgFaxadfYjzIfGp2grZPFezy_sknVY26dZmHYtTH0uEvvpUweTe0WndovuJxP9iIGRawRWd42jAUdiBMSxGcljkq1XL4blLz7uKf1wbeRdu2gyrfjaKHWZVDUmP4FLrmrOZV7SZV7P9bPdKIoAxrvGRn7wUOe_oFArU",
        "dp": "AzjL-EFIxtbVcCA_VBHxQQP0fm_1O4y6mXDc5ZI2kCZDYxfZfLMU3Qaz0k2AOM0JzPJzXfvZ4NX4Vx8tcqVXZjm2ILKDnOUBxNgws5wXw6pqgmS4q7snKi3t4OOCJkb05BYo6QMiDwtz6Bfx4vm06RWWhv8xCXuQuK_juH0Ba8s",
        "qi": "volSZ6zc0QUh0rw0YgkGX1T86tRlKdXOoBKpSE2Xdumfi_TcdhODLmzJsNrR_vyG1xuClJkr7l504e3pF7_HqPQ9IIX7QRgWNhQLKwJMevxzjnCI92G4ZByO_BeEgAD88qIuvLpTWUWndFXSDH45OV-duIAZUkM1Tx6eux6wQBM",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "qB45SzWy292aXNtod3d_YS3i31o_qFLXerOgR7dYwHZdCrj237wtz7BrA73-A-y-eJpMr_Pi0oeKXv5CaLdEZm0elwqiaWPjopoz-jZIiczAbrHNH9QxDhob7ILFnF6esEcN8F2OEluhmNmvNpEbk1WFh2AhmBdfkjuiIKE8UK3qrOnwplKn6McPk4vDPdVel5utYaYDI33t0sBGn5J4XF0MrpPEFS2MH-eeRgTlAgAM-x3bpZbk6XAtlNvoiX2GWa0hCDIgBq3AfoHyFxmqicXOV-UT13ETOd3gDLEgfBDgXxviZ8m5pkXOq5Rc0XLvsbBHb1hvnLLVrgGWpTjnew",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "http://www.myopenedx.com/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "JwTlRUcLIWFm9Uz9K9NinH3I"
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

# Delivery settings for ERB
EVENT_ROUTING_BACKEND_BATCHING_ENABLED = True
EVENT_ROUTING_BACKEND_BATCH_SIZE = 100
EVENT_ROUTING_BACKEND_BATCH_INTERVAL = 5

# Configuration needed for openedx-event-sink-clickhouse
EVENT_SINK_CLICKHOUSE_BACKEND_CONFIG = {
	"url": "http://clickhouse:8123",
	"username": "ch_cms",
	"password": "Zyw4LX5MdvEmenXP1hTm2jye",
	"database": "event_sink",
	"timeout_secs": 5
}
SUPERSET_CONFIG = {
	"service_url": "http://superset.www.myopenedx.com",
	"username": "Hlezksj7t2Nz",
	"password": "AdYCltNt8FqSvEm4XX9S8BFt",
}
EVENT_SINK_CLICKHOUSE_PII_MODELS = ['user_profile', 'external_id', 'auth_user']

ASPECTS_INSTRUCTOR_DASHBOARDS = [{'name': 'Course Dashboard', 'slug': 'course-dashboard', 'uuid': 'c0e64194-33d1-4d5a-8c10-4f51530c5ee9', 'allow_translations': True}, {'name': 'At-Risk Learners Dashboard', 'slug': 'learner-groups', 'uuid': '8661d20c-cee6-4245-9fcc-610daea5fd24', 'allow_translations': True}, {'name': 'Individual Learner Dashboard', 'slug': 'individual-learner', 'uuid': 'abae8a25-1ba4-4653-81bd-d3937a162a11', 'allow_translations': True}]
SUPERSET_DASHBOARD_LOCALES = ['ar', 'da', 'de_DE', 'el', 'en', 'es_419', 'es_ES', 'fr_CA', 'he', 'hi', 'id', 'it_IT', 'pt_BR', 'pt_PT', 'ru', 'th', 'tr_TR', 'uk', 'zh_CN']
SUPERSET_SHOW_INSTRUCTOR_DASHBOARD_LINK = True

try:
    not OPEN_EDX_FILTERS_CONFIG
except NameError:  # OPEN_EDX_FILTERS_CONFIG is not defined
    OPEN_EDX_FILTERS_CONFIG = {}
if not OPEN_EDX_FILTERS_CONFIG.get("org.openedx.learning.instructor.dashboard.render.started.v1"):
    OPEN_EDX_FILTERS_CONFIG["org.openedx.learning.instructor.dashboard.render.started.v1"] = {
        "fail_silently": False,
        "pipeline": [],
    }
OPEN_EDX_FILTERS_CONFIG["org.openedx.learning.instructor.dashboard.render.started.v1"]["pipeline"].append("platform_plugin_aspects.extensions.filters.AddSupersetTab")






EVENT_SINK_CLICKHOUSE_COURSE_OVERVIEWS_ENABLED = True
EVENT_SINK_CLICKHOUSE_TAG_ENABLED = True
EVENT_SINK_CLICKHOUSE_TAXONOMY_ENABLED = True
EVENT_SINK_CLICKHOUSE_OBJECT_TAG_ENABLED = True
EVENT_SINK_CLICKHOUSE_COURSE_ENROLLMENT_ENABLED = True

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
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "2ZctDNexJc76sE0OplutuvlY"
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

ALLOWED_HOSTS = [
    ENV_TOKENS.get("CMS_BASE"),
    "cms",
]
CORS_ORIGIN_WHITELIST.append("http://studio.www.myopenedx.com")

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://www.myopenedx.com"

# MFE-specific settings

COURSE_AUTHORING_MICROFRONTEND_URL = "http://apps.www.myopenedx.com/authoring"


LOGIN_REDIRECT_WHITELIST.append("apps.www.myopenedx.com")
CORS_ORIGIN_WHITELIST.append("http://apps.www.myopenedx.com")
CSRF_TRUSTED_ORIGINS.append("http://apps.www.myopenedx.com")

COURSE_AUTHORING_MICROFRONTEND_URL = "http://studio.www.myopenedx.com/authoring"
ENABLE_COMPREHENSIVE_THEMING = True
COMPREHENSIVE_THEME_DIRS.extend(['/openedx/themes/ednx-saas-themes/edx-platform', '/openedx/themes/ednx-saas-themes/edx-platform/bragi-children'])
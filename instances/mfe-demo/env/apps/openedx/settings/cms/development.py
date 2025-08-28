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
MEILISEARCH_PUBLIC_URL = "https://meilisearch.mfe-demo.phd.opencraft.hosting"
MEILISEARCH_INDEX_PREFIX = "tutor_"
MEILISEARCH_API_KEY = "ce0bcbd4f6a94c2c69dddae71bb0b4f9ef061788238286cfed48dc4693d8a0ba"
MEILISEARCH_MASTER_KEY = "1fbvbyA4fTalFnWjXmLZ6NT9"
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
CONTACT_MAILING_ADDRESS = "Picasso Harmony Drydock Experimentation - https://mfe-demo.phd.opencraft.hosting"
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


JWT_AUTH["JWT_ISSUER"] = "https://mfe-demo.phd.opencraft.hosting/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "2eM0xxD3FN2TsSF6qc6xmWfa"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "Pd96GclpP60_j8EhNtslpcZrFJ-p_Q1P1Spdi1UlU8zCH16PVuVlQFzi-_zznMWhjk1AEGl7Vu_dlOBXBOwYhaJXqht0HeGH1K1s27BPFYVeWxJP6m7Xs_NbgkgiYiBENBGw2o7VGu_WNbtotUC_9sqXq_K_RUIr9xeQP3ms6gp0tuxjjUx7E26-MesBrkLoptS6l_r44IoseffEidrufEr_pFlouPAlb20Ci1eBalidSB_oP7yAF6TSDGG4-UvTNU83aamIhwkBFOwpUP8CUmGFkxPUHGB4e4AhwzOsrcVfbgR-3G8E_vrjakt-DBA-eLoMgTpNqp8CQUubGCAWGQ",
        "n": "n-8eFOqGI88faXCsIksL0qUTJ4wnJK9-yHfmNYqZM53qrSaT6nsGDkdRnO1lscfiUGaRvLBKpDXDBX3zAf2CsXQwgro2LIY6GbMTf541P__gqcxfr9uCvoqlm5dxITShB9_mmTBcgbIaWVB_eLbuFU9ytSpCHYnL3yji5AKhEJ6aSW6JGFQ1ne784aQwPA6IDJsc_QKchmaFOOyt0DVULWbRjJkobOmosGwaSnPSNnRVj5gkiAg5m1EMPEqtPFcxdLV1_BP53ptbcNE4Mdjbzrm6O7L6_3gnoDYS1z8KmuhAMrJefjOLIGb3O3jHgJuupBszCl7PFLZD5aFa7cqhfQ",
        "p": "uixGqWA4bUgrpTtq55bsV5s7zwkbx7mHWV6NQR5pLHn5q_THYzhaP_n0Krvwtozg1kbXTPBJ-hEBaxoYDYvG14xv7iWu4pE5PnZsiV7kXT-LKcptsIZpvBiBoyvYI19T7rpyAB88YHnFL0SUxaDwAdxCed6X7z4kW5mUIYdcLOc",
        "q": "2-t3nYviGsScK3AXcU2WHTNXqCHY-C9oewhPzzmgxlpqit9v5i2--4H1n7Sy1tKHhqCbCP2yAyiaXue31IwlW6cZ4kxHONvq6BIHKW4-eNm9atrzwWns1CK1SrNx49iBv264eVdAqJS9vvIn9PQ5p2Yz_O3qEEY8ekwIagKKLfs",
        "dq": "QfZRbV7MlazNDrZTQbe8w8tnilWEp4RIuUZX8dbeI0BxXnAANzEXbIahbqKbVZXV8opvlfXKE-p0yuyDlevnNKNdPyQT5LkJr0vg_AtGD6d3ifpcTHICB-rVJ6_FBEsnN4z1JegGy8m5U_F8DJvIQy6Df2S45OK8Nw5hI7LZUUs",
        "dp": "Q4QBEDXD4OXWZjK5H0mdZlv2gauk9nZy_lcK1P3JWIbXo6O-l139ZMwp30GPFzTZ6PuB4vYVbemy4Ptyk58IOm1EvlHOLX5LCzr5O4w9Nw_vUPWHeAgW2k7s3Jbu6E0O7DmTVDX_uGEQwIaXiWBHCfWt6fJumSWpG8sDbHFhXSs",
        "qi": "JKc9xVdcSevs1WQ-XLO00F0y8T0VN_Rmu-gqulA1s7RGP9szO8nA3hiuxLhbqQ515A3xUJjSC7uAO3mlkxvGPhaCCcIhl913-T6Mw98kN2e8HAtUhDm1JR78ZzJ971vKLIeqqAGIHIAQLexPhnG1rcHQGXFtCm0nvLoxo9nA55Y",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "n-8eFOqGI88faXCsIksL0qUTJ4wnJK9-yHfmNYqZM53qrSaT6nsGDkdRnO1lscfiUGaRvLBKpDXDBX3zAf2CsXQwgro2LIY6GbMTf541P__gqcxfr9uCvoqlm5dxITShB9_mmTBcgbIaWVB_eLbuFU9ytSpCHYnL3yji5AKhEJ6aSW6JGFQ1ne784aQwPA6IDJsc_QKchmaFOOyt0DVULWbRjJkobOmosGwaSnPSNnRVj5gkiAg5m1EMPEqtPFcxdLV1_BP53ptbcNE4Mdjbzrm6O7L6_3gnoDYS1z8KmuhAMrJefjOLIGb3O3jHgJuupBszCl7PFLZD5aFa7cqhfQ",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "https://mfe-demo.phd.opencraft.hosting/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "2eM0xxD3FN2TsSF6qc6xmWfa"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = False
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
STUDIO_NAME = "Picasso Harmony Drydock Experimentation - Studio"

CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_cms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_cms",
}

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "tEOaPeM6YK4tPhlLnqG7FSkR"
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

LMS_BASE = "mfe-demo.phd.opencraft.hosting:8000"
LMS_ROOT_URL = "http://" + LMS_BASE

CMS_BASE = "studio.mfe-demo.phd.opencraft.hosting:8001"
CMS_ROOT_URL = "http://" + CMS_BASE

MEILISEARCH_PUBLIC_URL = "https://meilisearch.mfe-demo.phd.opencraft.hosting:7700"

# Authentication
SOCIAL_AUTH_EDX_OAUTH2_KEY = "cms-sso-dev"
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = LMS_ROOT_URL

FEATURES["PREVIEW_LMS_BASE"] = "preview.mfe-demo.phd.opencraft.hosting:8000"

# Setup correct webpack configuration file for development
WEBPACK_CONFIG_PATH = "webpack.dev.config.js"

ENABLE_COMPREHENSIVE_THEMING = True
COMPREHENSIVE_THEME_DIRS.extend(['/openedx/themes/ednx-saas-themes/edx-platform', '/openedx/themes/ednx-saas-themes/edx-platform/bragi-children'])
# MFE-specific settings

COURSE_AUTHORING_MICROFRONTEND_URL = "http://apps.mfe-demo.phd.opencraft.hosting:2001/authoring"
CORS_ORIGIN_WHITELIST.append("http://apps.mfe-demo.phd.opencraft.hosting:2001")
LOGIN_REDIRECT_WHITELIST.append("apps.mfe-demo.phd.opencraft.hosting:2001")
CSRF_TRUSTED_ORIGINS.append("http://apps.mfe-demo.phd.opencraft.hosting:2001")

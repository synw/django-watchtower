from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

redis_conf = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}

REDIS = getattr(settings, 'WT_REDIS', redis_conf)

SITE_SLUG = getattr(settings, 'SITE_SLUG')

SEPARATOR = getattr(settings, 'WT_SEPARATOR', "#!#")

FREQUENCY = getattr(settings, 'WT_FREQUENCY', 5)

VERBOSITY = getattr(settings, 'WT_VERBOSITY', 0)

STOP = getattr(settings, 'WT_STOP', False)

EXCLUDE = getattr(settings, 'WT_EXCLUDE', ["/admin/jsi18n/", "/media/"])

COLLECTOR = getattr(settings, 'WT_COLLECTOR', True)

DBS = getattr(settings, 'WT_DATABASES', None)
if DBS is None:
    raise ImproperlyConfigured("Please configure a database for Watchtower")

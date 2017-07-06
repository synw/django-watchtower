from django.conf import settings


redis_conf = {
    "host": "localhost",
    "port": 6379,
    "db": 0,
}

INFLUX = getattr(settings, "WT_INFLUX", None)

REDIS = getattr(settings, 'WT_REDIS', redis_conf)

SITE_SLUG = getattr(settings, 'SITE_SLUG')

SEPARATOR = getattr(settings, 'WT_SEPARATOR', "#!#")

FREQUENCY = getattr(settings, 'WT_FREQUENCY', 5)

VERBOSITY = getattr(settings, 'WT_VERBOSITY', 0)
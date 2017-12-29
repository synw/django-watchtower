# Django Watchtower

Collect metrics and events from Django.

How it works: numbers taken out from Django are stored in Redis and a collector saves them in some
database(s)

**Metrics**: each hit is saved with fields ip, request time, query time, user_agent, geographical information and [more](#collected-data)

**Events**: logs, actions on registered models and user defined events are stored 
(with [django-mqueue](https://github.com/synw/django-mqueue))

## Install

Install the GeoIp tools:

   ```bash
   cd /my/geo/folder
   wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
   wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
   ```
   
Unzip and add to settings.py:

   ```python
   GEOIP_PATH = "/my/geo/folder"
   ```

Install the dependencies: 

   ```bash
   pip install redis influxdb geoip2 django-user-agents django-mqueue
   ```

[Configure mqueue](http://django-mqueue.readthedocs.io/en/latest/usage/registered_models.html) to record what you want

Add to installed apps:

   ```python
   "django_user_agents",
   "mqueue",
   "watchtower",
   ```

Add the middlewares:

   ```python
   MIDDLEWARE_CLASSES = (
    'django_user_agents.middleware.UserAgentMiddleware',
    'watchtower.middleware.HitsMiddleware',
    # ... other middlewares
   )
   ```
   
Set the Django databases:

   ```python
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'hits': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'hits.sqlite3'),
    }
   }

   DATABASE_ROUTERS = ['watchtower.router.HitsRouter']
   ```

Add to settings.py:
   ```python
   
   # required
   SITE_SLUG = "mysite"
   
   # to pipe events into watchtower
   MQUEUE_HOOKS = {
    "redis": {
        "path": "mqueue.hooks.redis",
        "host": "localhost",
        "port": 6379,
        "db": 0,
    }
   }
   # set the databases to use
   WT_DATABASES = {
    # required: at least one database
    "default": {
        "type": "django",
        "hits_db": "hits" # name of a DATABASE in settings
    },
   # defaults:
   WT_REDIS = {
    "addr": "localhost:6379",
    "db": 0
   }
   ```

Options to exclude certain paths from hits recording:

   ```python
   WT_EXCLUDE = ("/path/not/recorded/",)
   ```
# Run the collector

   ```python
   python3 manage.py collect
   ```

Note: it is possible to save the data directly into the database not using Redis and the collector with the setting:

   ```python
   WT_COLLECTOR = False
   ```

Do not use this setting in production: it will not work when `DEBUG` is `False`

# Collected data

   ```javascript
   {
    "site": "mysite",
    "user": "admin",
    "request_time": 35,
    "status_code": 200,
    "doc_size": 3912,
    "ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "method": "GET",
    "view": "AddPostView",
    "module": "qcf.views",
    "is_superuser": true,
    "is_authenticated": true,
    "reason_phrase": "OK",
    "ua": {
     "os_version": "",
     "is_pc": true,
     "browser_version": "55.0",
     "is_mobile": false,
     "os": "Ubuntu",
     "is_tablet": false,
     "is_bot": false,
     "device": "Other",
     "is_touch": false,
     "browser": "Firefox"
    },
    "geo": {
     "latitude": 0,
     "postal_code": "",
     "country_code": "",
     "region": "",
     "dma_code": "",
     "country_name": "",
     "longitude": 0,
     "city": ""
    },
    "is_staff": true,
    "referer": "",
    "path": "/",
    "queries_time": 2,
    "num_queries": 1
   }
   ```

# Django Watchtower

Collect metrics and events from Django.

How it works: numbers taken out from Django are stored in Redis and a collector saves them in 
a database

**Metrics**: each hit is saved with fields ip, request time, query time, user_agent, geographical information and 
[more](#collected-data)

**Events**: logs, actions on registered models and user defined events are stored

## Supported databases

- [x] Django databases
- [x] Influxdb
- [ ] Rethinkdb

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
   pip install redis influxdb django-user-agents django-mqueue
   ```

[Configure mqueue](http://django-mqueue.readthedocs.io/en/latest/usage/registered_models.html) to record what you want

Add to installed apps:

   ```python
   "mqueue",
   "watchtower",
   ```

Add the middleware:

   ```python
   MIDDLEWARE_CLASSES = (
    'watchtower.middleware.HitsMiddleware',
    # ... other middlewares
   )
   ```

Add to settings.py:
   ```python
   # to pipe events into watchtower
   MQUEUE_HOOKS = {
    "redis": {
        "path": "mqueue.hooks.redis",
        "host": "localhost",
        "port": 6379,
        "db": 0,
    }
   }
   # declare the databases
   WT_DATABASES = {
    "default": {
        "type": "django",
        "hits_db": "hits" # name of the DATABASE
    },
    "timeseries": {
        "type": "influxdb",
        "host": "localhost",
        "port": 8086,
        "user": "admin",
        "password": "admin",
        "hits_db": "hits",
        "events_db": "events",
    }
   }
   # defaults:
   WT_REDIS = {
    "addr": "localhost:6379",
    "db": 0
   }
   ```

Create your Influxdb databases for hits and events

Options to exclude certain paths from hits recording:

   ```python
   WT_EXCLUDE = ("/path/not/recorded/",)
   ```
# Run the collector

   ```python
   python3 manage.py collect
   ```

# Collected data

   ```javascript
   {
    "site": "mysite",
    "user": "admin",
    "request_time": "35",
    "status_code": "200",
    "doc_size": "3912",
    "ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
    "method": "GET",
    "view": "AddPostView",
    "module": "qcf.views",
    "is_superuser": "true",
    "is_authenticated": "true",
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
    "is_staff": "true",
    "referer": "",
    "path": "/",
    "queries_time": "2",
    "num_queries": "1"
   }
   ```

# Visualization dashboards

[Grafana dashboards](https://github.com/synw/django-watchtower/tree/master/dashboards) are available: the overview dashboard:

![Overview dashboard](https://github.com/synw/django-watchtower/raw/master/doc/img/overview.png)

The queries dashboard:

![Queries dashboard](https://github.com/synw/django-watchtower/raw/master/doc/img/queries.png)

Note: this is work in progress and some numbers in the dashboards are not acurate due to my lack of knowledge on how to query
data in an appropriate maner in Grafana. Help is welcome here.

# Todo

- [ ] More dashboards

# Django Watchtower

Collect metrics and events from Django.

How it works: numbers taken out from Django are stored in Redis and a collector saves them in 
Influxdb at a regular interval and cleans the Redis keys 

**Metrics**: each hit is saved with fields ip, request time, query time, user_agent, method, referer, user, view, module and more

**Events**: logs, actions on registered models and user defined events are stored

## Dependencies

- [Redis](https://redis.io/): the in-memory k/v store
- [Influxdb](https://www.influxdata.com/): timeseries database
- [Django Hitsmon](https://github.com/synw/django-mqueue): to produce hits and metrics
- [Django Mqueue](https://github.com/synw/django-hitsmon): to produce events

## Install

Install django-mqueue and the redis drivers:

   ```bash
   pip install redis django-mqueue
   ```

[Configure mqueue](http://django-mqueue.readthedocs.io/en/latest/usage/registered_models.html) to record what you want

Install django-hitsmon (not yet on pip):

   ```bash
   pip install git+git://github.com/synw/django-hitsmon
   ```

Add to installed apps:

   ```python
   "mqueue",
   "hitsmon",
   "watchtower",
   ```

Add the middleware:

   ```python
   MIDDLEWARE_CLASSES = (
    'hitsmon.middleware.HitsMiddleware',
    # ... other middlewares
   )
   ```

Add to settings.py:
   ```python
   MQUEUE_HOOKS = {
    "redis": {
        "path": "mqueue.hooks.redis",
        "host": "localhost",
        "port": 6379,
        "db": 0,
    }
   }
   WT_INFLUX = {
    "addr": "localhost:8086",
    "user": "admin",
    "password": "pwd",
    "hits_db": "hits",
    "events_db": "events",
   }
   WT_REDIS = {
    "addr": "localhost:6379",
    "db": 0
   }
   ```

Create your Influxdb databases for hits and events

Options to exclude certain paths from hits recording:

   ```python
   HITSMON_EXCLUDE = ("/path/not/recorded/",)
   ```
# Run the collector

   ```python
   python3 manage.py collect
   ```

Note: the collector uses a Go module: it will work on Linux. For other systems you would have to compile it
from [the source](https://github.com/synw/django-watchtower/tree/master/watchtower/collector/src)

# Visualization dashboards

[Grafana dashboards](https://github.com/synw/django-watchtower/tree/master/dashboards) are available: the overview dashboard:

![Overview dashboard](https://github.com/synw/django-watchtower/raw/master/doc/img/overview.png)

The queries dashboard:

![Queries dashboard](https://github.com/synw/django-watchtower/raw/master/doc/img/queries.png)

Note: this is work in progress and some numbers in the dashboards might be innacurate

# Todo

- [ ] More dashboards

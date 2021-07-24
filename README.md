# Django Watchtower

Collect hits metrics from Django.

How it works: numbers taken out from Django are stored in Redis and a collector saves them in some
database(s)

**Metrics**: each hit is saved with fields ip, request time, query time, user_agent, geographical 
information and [more](#collected-data)

## Install

   ```bash
   pip install django-watchtower
   ```

Add to installed apps:

   ```python
   "django_user_agents",
   "watchtower",
   ```

Add the middlewares:

   ```python
   MIDDLEWARE_CLASSES = (
      # ... other middlewares
    'django_user_agents.middleware.UserAgentMiddleware',
    'watchtower.middleware.HitsMiddleware',
   )
   ```

Set the Django databases:

   ```python
   DATABASES = {
    'default': # ...,
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
  
   # set the databases to use: required
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

Install the GeoIp tools (optional): [get the geoip database](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)

Unzip and add to settings.py:

   ```python
   GEOIP_PATH = "/my/geo/folder"
   ```
   
Make the migrations:

   ```
   python3 manage.py migrate watchtower --database=hits
   ```
   
### Additional settings

Exclude certain paths from hits recording:

   ```python
   WT_EXCLUDE = ["/path/not/recorded/"]
   # default:
   # ["/admin/jsi18n/", "/media/"]
   ```

Note: this will exclude all paths that start with the provided values

Change the default collector save interval:

   ```python
   WT_FREQUENCY = 30
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

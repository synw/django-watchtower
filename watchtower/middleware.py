# -*- coding: utf-8 -*-

import inspect
import time
import redis
from threading import Thread
from django.db import connection
from watchtower.db import dispatch
from watchtower import serializer, conf as CONF
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

R = redis.StrictRedis(
    host=CONF.REDIS["host"], port=CONF.REDIS["port"], db=CONF.REDIS["db"])

HITNUM = int(time.time())


class HitsMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, *args, **kwargs):
        global CONF
        """
        Credits: https://github.com/bitlabstudio/django-influxdb-metrics/blob/master/influxdb_metrics/middleware.py
        """
        if CONF.STOP:
            return
        view = view_func
        if not inspect.isfunction(view_func):
            view = view.__class__
        try:
            request._view_module = view.__module__
            request._view_name = view.__name__
            request._start_time = time.time()
        except AttributeError:
            pass

    def process_response(self, request, response):
        global CONF
        global HITNUM
        if CONF.STOP:
            return response
        data = {}
        data["path"] = request.path_info
        for expath in CONF.EXCLUDE:
            if data["path"].startswith(expath):
                return response
        doc_size = 0
        try:
            doc_size = len(response.content)
        except Exception:
            pass
        total_time = 0
        for query in connection.queries:
            query_time = query.get('time')
            if query_time is None:
                query_time = 0
            total_time += float(query_time)
        total_time = int(total_time * 1000)
        num_queries = len(connection.queries)
        data["method"] = request.method
        data['ip'] = request.META['REMOTE_ADDR']
        data['user_agent'] = "Unknown"
        if "HTTP_USER_AGENT" in request.META:
            data["user_agent"] = request.META['HTTP_USER_AGENT']
        data['referer'] = ''
        if 'HTTP_REFERER' in data:
            data['referer'] = request.META['HTTP_REFERER']
        data['user'] = 'Anonymous'
        is_authenticated = "false"
        if request.user.is_authenticated():
            is_authenticated = "true"
            data['user'] = request.user.username
        is_staff = "false"
        is_superuser = "false"
        if request.user.is_authenticated():
            is_authenticated = "true"
            if request.user.is_staff:
                is_staff = "true"
            if request.user.is_superuser:
                is_superuser = "true"
        request_time = 0
        if hasattr(request, '_start_time'):
            request_time = int((time.time() - request._start_time) * 1000)
        data["is_superuser"] = is_superuser
        data["is_staff"] = is_staff
        data["is_authenticated"] = is_authenticated
        data["ajax"] = request.is_ajax()
        data["request_time"] = request_time
        try:
            data["view"] = request._view_name
        except Exception:
            data["view"] = ""
        try:
            data["module"] = request._view_module
        except Exception:
            data["module"] = ""
        data["status_code"] = response.status_code
        data["reason_phrase"] = response.reason_phrase
        data["doc_size"] = doc_size
        data["queries_time"] = total_time
        data["num_queries"] = num_queries
        data["content_length"] = doc_size
        ua = {
            "is_mobile": request.user_agent.is_mobile,
            "is_pc": request.user_agent.is_pc,
            "is_tablet": request.user_agent.is_tablet,
            "is_bot": request.user_agent.is_bot,
            "is_touch": request.user_agent.is_touch_capable,
            "browser": request.user_agent.browser.family,
            "browser_version": request.user_agent.browser.version_string,
            "os": request.user_agent.os.family,
            "os_version": request.user_agent.os.version_string,
            "device": request.user_agent.device.family,
        }
        data["ua"] = ua
        name = CONF.SITE_SLUG + "_hit" + str(HITNUM)
        data["geo"] = serializer.getGeoData(data['ip'])
        if CONF.COLLECTOR is True:
            hit = serializer.pack(data)
            R.set(name, hit)
        else:
            thread = Thread(target=dispatch, args=([data],))
            thread.start()
        HITNUM += 1
        return response

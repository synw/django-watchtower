# -*- coding: utf-8 -*-

from __future__ import print_function
from django.conf import settings
from watchtower.db import orm, influx
from watchtower.conf import DBS


def dispatch(hits):
    global DBS
    for key in DBS:
        db = DBS[key]
        if "hits_db" in db:
            if db["type"] == "django":
                try:
                    djdb = db["hits_db"]
                except:
                    print("Database ", db, "not found")
                orm.write(djdb, hits)
            elif db["type"] == "influxdb":
                influx.write(hits)

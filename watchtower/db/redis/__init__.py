# -*- coding: utf-8 -*-

import json
import time
import redis
from watchtower.conf import SITE_SLUG, DBS
from watchtower.serializer import decodeHitRow, decodeEventRow


def getHits(r):
    prefix = SITE_SLUG + "_hit*"
    hits = []
    for key in r.scan_iter(prefix):
        val = r.get(key)
        r.delete(key)
        hit = decodeHitRow(val)
        hits.append(hit)
    return hits


def getEvents(r):
    global SITE_SLUG
    prefix = SITE_SLUG + "_event*"
    events = []
    for key in r.scan_iter(prefix):
        val = r.get(key)
        r.delete(key)
        event = decodeEventRow(val)
        events.append(event)
    return events

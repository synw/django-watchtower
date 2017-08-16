# -*- coding: utf-8 -*-

import json
import time
import redis
from watchtower.conf import SITE_SLUG, VERBOSITY, DBS
from watchtower.serializer import decodeRow


def getHits(r):
    global SITE_SLUG
    global VERBOSITY
    prefix = SITE_SLUG + "_hit*"
    hits = []
    for key in r.scan_iter(prefix):
        val = r.get(key)
        r.delete(key)
        hit = decodeRow(val)
        hits.append(hit)
    return hits

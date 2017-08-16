# -*- coding: utf-8 -*-

import json
from django.contrib.gis.geoip2 import GeoIP2
from watchtower.conf import SITE_SLUG, SEPARATOR


G = GeoIP2()


def pack(data):
    global SITE_SLUG
    global G
    sep = "#!#"
    h = (
        SITE_SLUG,
        data["path"],
        data["method"],
        data["ip"],
        data["user_agent"],
        str(data["is_authenticated"]).lower(),
        str(data["is_staff"]).lower(),
        str(data["is_superuser"]).lower(),
        data["user"],
        data["referer"],
        data["view"],
        data["module"],
        str(data["status_code"]),
        data["reason_phrase"],
        str(data["request_time"]),
        str(data["doc_size"]),
        str(data["num_queries"]),
        str(data["queries_time"]),
        json.dumps(data["ua"]),
    )
    hit = str.join(sep, h)
    return hit


def decodeRow(row):
    global SEPARATOR
    global G
    vals = row.decode().split(SEPARATOR)
    data = {}
    data["site"] = vals[0]
    data["path"] = vals[1]
    data["method"] = vals[2]
    data["ip"] = vals[3]
    data["user_agent"] = vals[4]
    data["is_authenticated"] = vals[5]
    data["is_staff"] = vals[6]
    data["is_superuser"] = vals[7]
    data["user"] = vals[8]
    data["referer"] = vals[9]
    data["view"] = vals[10]
    data["module"] = vals[11]
    data["status_code"] = vals[12]
    data["reason_phrase"] = vals[13]
    data["request_time"] = vals[14]
    data["doc_size"] = vals[15]
    data["num_queries"] = vals[16]
    data["queries_time"] = vals[17]
    data["ua"] = json.loads(vals[18])
    # geo data
    geo = {
        "latitude": 0,
        "country_name": "",
        "longitude": 0,
        "postal_code": "",
        "dma_code": "",
        "city": "",
        "country_code": "",
        "region": ""
    }
    if data["ip"].startswith("127.") is False and data["ip"].startswith("192.") is False:
        geo = G.city(data["ip"])
    data["geo"] = geo
    return data
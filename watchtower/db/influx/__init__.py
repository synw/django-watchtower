# -*- coding: utf-8 -*-

import json
from threading import Thread
from influxdb import InfluxDBClient
from watchtower.conf import INFLUX, SITE_SLUG


if INFLUX is not None:
    CLI = InfluxDBClient(
        INFLUX["host"],
        INFLUX["port"],
        INFLUX["user"],
        INFLUX["password"],
        INFLUX["hits_db"],
        timeout=5,
        ssl=False
    )
    ECLI = InfluxDBClient(
        INFLUX["host"],
        INFLUX["port"],
        INFLUX["user"],
        INFLUX["password"],
        INFLUX["events_db"],
        timeout=5,
        ssl=False
    )


def write_events(points):
    global ECLI
    try:
        ECLI.write_points(points)
    except Exception as err:
        raise err


def write_hits(points):
    global CLI
    try:
        CLI.write_points(points)
    except Exception as err:
        raise err


def process_events(events):
    points = []
    for event in events:
        tags = {
            "service": "django",
            "domain": SITE_SLUG,
            "name": event["name"],
        }
        if "event_class" in event:
            tags["class"] = event["event_class"]
        if "content_type" in event:
            tags["content_type"] = event["content_type"]
        if "obj_pk" in event:
            tags["obj_pk"] = event["obj_pk"]
        if "user" in event:
            tags["user"] = event["user"]
        if "url" in event:
            tags["url"] = event["url"]
        if "admin_url" in event:
            tags["admin_url"] = event["admin_url"]
        if "notes" in event:
            tags["notes"] = event["notes"]
        if "bucket" in event:
            tags["bucket"] = event["bucket"]
        if "data" in event:
            tags["data"] = event["data"]
        if "scope" in event:
            tags["scope"] = event["scope"]
        data = {
            "measurement": "event",
            "tags": tags,
            "fields": {
                "num": 1,
            }
        }
        points.append(data)
    write_events(points)


def process_hits(hits):
    points = []
    for hit in hits:
        data = {
            "measurement": "hits",
            "tags": {
                "service": "django",
                "domain": SITE_SLUG,
                "user": hit["user"],
                "path": hit["path"],
                "referer": hit["referer"],
                "user_agent": hit["user_agent"],
                "method": hit["method"],
                "authenticated": hit["is_authenticated"],
                "staff": hit["is_staff"],
                "superuser": hit["is_superuser"],
                "status_code": hit["status_code"],
                "view": hit["view"],
                "module": hit["module"],
                "ip": hit["ip"],
                "os": hit["ua"]["os"],
                "os_version": hit["ua"]["os_version"],
                "is_pc": hit["ua"]["is_pc"],
                "is_bot": hit["ua"]["is_bot"],
                "is_tablet": hit["ua"]["is_tablet"],
                "is_mobile": hit["ua"]["is_mobile"],
                "is_touch": hit["ua"]["is_touch"],
                "browser": hit["ua"]["browser"],
                "device": hit["ua"]["device"],
                "country": hit["geo"]["country_name"],
                "latitude": float(hit["geo"]["latitude"]),
                "longitude": float(hit["geo"]["longitude"]),
                "region": hit["geo"]["region"],
                "city": hit["geo"]["city"]
            },
            "fields": {
                "num": 1,
                "request_time": hit["request_time"],
                "doc_size": hit["doc_size"],
                "num_queries": hit["num_queries"],
                "queries_time": hit["queries_time"],
            }
        }
        points.append(data)
    write_hits(points)

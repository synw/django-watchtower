# -*- coding: utf-8 -*-

import time
import json
from threading import Thread
from django.db import transaction
from watchtower.models import Hit
from watchtower.conf import VERBOSITY


def convertBool(val):
    if val == "false":
        return False
    elif val == "true":
        return True
    else:
        return False


@transaction.atomic
def write(db, hits):
    global VERBOSITY
    i = len(hits)
    hit_objs = []
    for hit in hits:
        if VERBOSITY > 0 and i > 0:
            if VERBOSITY > 1:
                print(json.dumps(hit, indent=2))
        hit_obj = Hit(
            path=hit["path"],
            method=hit["method"],
            ip=hit["ip"],
            user_agent=hit["user_agent"],
            authenticated=convertBool(hit["is_authenticated"]),
            staff=convertBool(hit["is_staff"]),
            superuser=convertBool(hit["is_superuser"]),
            username=hit["user"],
            referer=hit["referer"],
            view=hit["view"],
            module=hit["module"],
            status_code=int(hit["status_code"]),
            reason_phrase=hit["reason_phrase"],
            request_time=float(hit["request_time"]),
            doc_size=hit["doc_size"],
            num_queries=int(hit["num_queries"]),
            queries_time=float(hit["queries_time"]),
            os=hit["ua"]["os"],
            os_version=hit["ua"]["os_version"],
            is_pc=convertBool(hit["ua"]["is_pc"]),
            is_bot=convertBool(hit["ua"]["is_bot"]),
            is_tablet=convertBool(hit["ua"]["is_tablet"]),
            is_mobile=convertBool(hit["ua"]["is_mobile"]),
            is_touch=convertBool(hit["ua"]["is_touch"]),
            browser=hit["ua"]["browser"],
            device=hit["ua"]["device"],
            country=hit["geo"]["country_name"],
            latitude=float(hit["geo"]["latitude"]),
            longitude=float(hit["geo"]["longitude"]),
            region=hit["geo"]["region"],
            city=hit["geo"]["city"]
        )
        hit_objs.append(hit_obj)
    Hit.objects.using(db).bulk_create(hit_objs)
    if i > 0 and VERBOSITY > 0:
        s = "s"
        if i == 1:
            s = ""
        t = time.strftime('%X')
        print(t, ":", "processed", i, "hit" + s)

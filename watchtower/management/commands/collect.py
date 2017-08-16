# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import redis
from django.core.management.base import BaseCommand
from watchtower.db import dispatch
from watchtower.db.redis import getHits
from watchtower.conf import FREQUENCY, VERBOSITY


class Command(BaseCommand):
    help = 'Start Watchtower collector'

    def handle(self, *args, **options):
        global VERBOSITY
        global FREQUENCY
        if VERBOSITY > 0:
            print("Collecting data ...")
        r = redis.Redis(host='localhost', port=6379, db=0)
        while True:
            hits = getHits(r)
            dispatch(hits)
            time.sleep(FREQUENCY)

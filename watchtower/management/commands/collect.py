# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import redis
from django.core.management.base import BaseCommand
from watchtower.db import dispatch
from watchtower.db.redis import getHits, getEvents
from watchtower.conf import FREQUENCY, VERBOSITY


class Command(BaseCommand):
    help = 'Start Watchtower collector'

    def handle(self, *args, **options):
        verbosity = options["verbosity"]
        if verbosity is None:
            verbosity = VERBOSITY
        if verbosity > 0:
            print("Collecting data ...")
        r = redis.Redis(host='localhost', port=6379, db=0)
        while True:
            hits = getHits(r)
            events = getEvents(r)
            dispatch(hits, events, verbosity)
            time.sleep(FREQUENCY)

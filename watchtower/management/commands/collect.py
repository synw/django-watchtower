from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
import subprocess
from django.conf import settings
from watchtower.conf import REDIS, INFLUX, SITE_SLUG, FREQUENCY, SEPARATOR, VERBOSITY


class Command(BaseCommand):
    help = 'Start Watchtower collector'

    def handle(self, *args, **options):
        if VERBOSITY > 0:
            print("Collecting data ...")
        pth = settings.BASE_DIR+"/watchtower/collector/"
        c=pth+'watchtower'
        cmd = [
            c,
            "-ra", REDIS["addr"],
            "-rdb", str(REDIS["db"]),
            "-ia", INFLUX["addr"],
            "-iu", INFLUX["user"],
            "-ip", INFLUX["password"],
            "-inh", INFLUX["hits_db"],
            "-ine", INFLUX["events_db"],
            "-f", str(FREQUENCY),
            "-s", SEPARATOR,
            "-d", SITE_SLUG,
            "-v", str(VERBOSITY)
            
        ]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in p.stdout:
            msg = str(line).replace("b'", "")
            msg = msg[0:-3]
            print(msg)
        p.wait()     
        return
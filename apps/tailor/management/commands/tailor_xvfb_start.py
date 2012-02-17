import os
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess

#DISPLAY_EXPORT = getattr(settings, 'DISPLAY_EXPORT', 'export DISPLAY=:0')
XVFB_PATH = getattr(settings, 'XVFB_PATH', '/usr/bin/Xvfb')
XVFB_START = getattr(settings, 'XVFB_START', ':0 -screen 0 640x480x32')

class Command(BaseCommand):
    help = "Start Xvfb from Command Line."

    def handle(self, *args, **options):
        call = [XVFB_PATH, XVFB_START]
        ret = subprocess.call(call, stdout=None, stderr=None)
        if ret > 0:
           print "Warning - result was %d" % ret
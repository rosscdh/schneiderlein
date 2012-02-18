import os
from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option

import subprocess

JAVA_PATH = getattr(settings, 'JAVA_PATH', '/usr/bin/java')
SELENIUM_PATH = getattr(settings, 'SELENIUM_PATH', 'bin/selenium-server-standalone-2.19.0.jar')

XVFB_PATH = getattr(settings, 'XVFB_PATH', '/usr/bin/Xvfb')
XVFB_START = getattr(settings, 'XVFB_START', ':0 -screen 0 1280x1024x24')


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--start-selenium',
            action='store_true',
            dest='start_selenium',
            default=True,
            help='Dont start Selenium Server'),
        make_option('--start-xvfb',
            action='store_true',
            dest='start_xvfb',
            default=True,
            help='Dont start Xvfb Server'),
        )
    help = "Start Schneiderlein services from the cli"

    def handle(self, *args, **options):

        if not os.getenv('DISPLAY'):
            os.putenv('DISPLAY', 'localhost:0.0')

        if options['start_xvfb'] == True:
           call = [XVFB_PATH, XVFB_START]
           ret = subprocess.Popen(call, stdout=None, stderr=None)
           if ret > 0:
              print "Warning - result was %s" % ret

        if options['start_selenium'] == True:
            cmd = '%s' % ( os.path.join(settings.PROJECT_DIR, SELENIUM_PATH), )
            call = [JAVA_PATH, "-jar", cmd]
            ret = subprocess.Popen(call, stdout=None, stderr=None)
            if ret > 0:
              print "Warning - result was %s" % ret

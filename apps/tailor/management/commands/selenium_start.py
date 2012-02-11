import os
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess

JAVA_PATH = getattr(settings, 'JAVA_PATH', '/usr/bin/java')
SELENIUM_PATH = getattr(settings, 'SELENIUM_PATH', 'bin/selenium-server-standalone-2.19.0.jar')

class Command(BaseCommand):
    help = "Start Selenium jar from Command Line."

    def handle(self, *args, **options):
        cmd = '%s' % ( os.path.join(settings.PROJECT_DIR, SELENIUM_PATH), )
        call = [JAVA_PATH, "-jar", cmd]
        ret = subprocess.call(call, stdout=None, stderr=None)
        if ret > 0:
           print "Warning - result was %d" % ret
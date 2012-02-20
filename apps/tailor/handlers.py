from django.core import serializers
import logging


class BuildHandler(logging.Handler): # Inherit from logging.Handler
  def emit(self, record):
    # record.message is the log message
    out = open("/tmp/file.xml", "w")
    out.write(str(record))
    out.close()
import time
import logging
from django.core import serializers
from django.core.signals import request_finished



class CuttingRoomHandler(logging.Handler): # Inherit from logging.Handler
    def emit(self, record):
        from apps.tailor.models import CuttingRoomLog

        thread_id = record.__dict__['thread']

        log, created = CuttingRoomLog.objects.get_or_create(thread=thread_id, defaults={'build_status': CuttingRoomLog.BS_INPROGRESS})

        # set the page only if it is specified and has not already been set
        if 'page' in record.__dict__ and (created or not log.page):
            log.page = record.__dict__['page']

        msg = dict({
            'msg': record.__dict__['msg'],
            'time': time.time(),
            'level': record.__dict__['levelname'],
            'msecs': record.__dict__['msecs'],
        })

        if record.__dict__['levelname'] == 'ERROR':
            log.build_status = CuttingRoomLog.BS_FAIL

        log.add_log(msg, 'logs')
        log.save()


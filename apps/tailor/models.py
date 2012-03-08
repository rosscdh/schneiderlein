from django.db import models
import datetime
from dateutil import relativedelta
from apps.page.models import Page
from apps.page.fields import JsonListField
from apps.tailor.signals import build_item_commence, build_item_complete


class CuttingRoomLog(models.Model):
    BS_FAIL = 0
    BS_SUCCESS = 1
    BS_INPROGRESS = 2
    BS_INVALID = 4
    BUILD_STATUS = (
        (BS_FAIL,'Failed'),
        (BS_SUCCESS,'Success'),
        (BS_INPROGRESS,'In Progress'),
        (BS_INVALID,'Invalid')
    )
    """
    Object to store build logs; JSON field allows for storage of multiple
    steps in the build process
    """
    thread = models.IntegerField()
    page = models.ForeignKey(Page,null=True, blank=True)
    date_start = models.DateTimeField(auto_now=True, auto_now_add=True)
    date_end = models.DateTimeField(auto_now=False, auto_now_add=False, null=True,blank=True)
    ran_for = models.BigIntegerField(null=True, blank=True)
    body = JsonListField(null=True, blank=True)
    build_status = models.IntegerField(choices=BUILD_STATUS, default=BS_INPROGRESS)

    def __unicode__(self):
        return u'%s %s' % (self.thread, self.build_status, )

    def add_log(self,value,name):
        name = name if name else 'items'
        if not self.body or not name in self.body:
            self.body = dict({name: []})

        if value not in self.body[name]:
            self.body[name].append(value)

        return self.body[name]

    def del_log(self,value,name):
        name = name if name else 'items'
        if name in self.body:
            if value in self.body[name]:
                self.body[name].remove(value)

        return self.body[name]


### ----- SIGNAL HANDLERS ----- ###
def build_item_commence_handler(sender, **kwargs):
    """signal intercept for builds"""
    thread_id = kwargs['thread']
    build_status = kwargs['build_status'] if 'build_status' in kwargs else CuttingRoomLog.BS_INPROGRESS

    log, created = CuttingRoomLog.objects.get_or_create(thread=thread_id, defaults={'build_status': build_status})


def build_item_complete_handler(sender, **kwargs):
    """signal intercept for builds"""
    thread_id = kwargs['thread']
    build_status = kwargs['build_status'] if 'build_status' in kwargs else CuttingRoomLog.BS_INVALID

    log = CuttingRoomLog.objects.get(thread=thread_id)

    log.date_end = datetime.datetime.now()
    difference = log.date_start - log.date_end
    log.ran_for = difference.microseconds

    # if its nto an illegal status (ie has failed)
    if log.build_status not in [CuttingRoomLog.BS_FAIL, CuttingRoomLog.BS_INVALID]:
        log.build_status = CuttingRoomLog.BS_SUCCESS

    log.save()

build_item_complete.connect(build_item_complete_handler)

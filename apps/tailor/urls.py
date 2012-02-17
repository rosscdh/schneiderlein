from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings


urlpatterns = patterns('apps.tailor.views',
    url(r'^process/(?P<process_name>.*)/$', 'start_process', name='tailor-start_process'),
)
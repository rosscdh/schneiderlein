from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    url(r'^xml/sitemap/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/tmp/', 'show_indexes': True}, name='page-sitemap_upload'),
)
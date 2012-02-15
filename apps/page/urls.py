from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

from views import admin_load_page_url


urlpatterns = patterns('',
    url(r'^load/remote/(?P<page_id>\d+)$', admin_load_page_url, name='page-load_remote'),
    url(r'^xml/sitemap/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/tmp/', 'show_indexes': True}, name='page-sitemap_upload'),
)
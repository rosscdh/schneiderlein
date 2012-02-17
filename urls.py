from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^pages/', include('apps.page.urls')),
    url(r'^tailor/', include('apps.tailor.urls')),
    url(r'^', include(admin.site.urls)),
)

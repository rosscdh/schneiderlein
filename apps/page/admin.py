from django.contrib import admin
from django.conf.urls.defaults import *
from models import Page, LoginPage
from views import admin_sitemap_import

class PageAdmin(admin.ModelAdmin):
        def get_urls(self):
            urls = super(PageAdmin, self).get_urls()
            host_admin_urls = patterns('',
                url(r'^sitemap/import/$', self.admin_site.admin_view(admin_sitemap_import), name='page.admin_sitemap_import',),
            )
            return host_admin_urls + urls

admin.site.register([LoginPage])
admin.site.register(Page, PageAdmin)
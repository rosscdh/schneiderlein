from django.contrib import admin
from django.conf.urls.defaults import *
from models import Page
from views import admin_sitemap_import


class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'is_child',)

    def get_urls(self):
        urls = super(PageAdmin, self).get_urls()
        host_admin_urls = patterns('',
            url(r'^sitemap/import/$', self.admin_site.admin_view(admin_sitemap_import), name='page.admin_sitemap_import',),
        )
        return host_admin_urls + urls

admin.site.register(Page, PageAdmin)
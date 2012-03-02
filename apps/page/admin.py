# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.conf.urls.defaults import *

from apps.sequence.models import Sequence

from models import Page
from views import admin_sitemap_import


# class SequenceInline(admin.TabularInline):
#     model = Page.sequence_tests.through
# 
# class StepTestInline(admin.TabularInline):
#     model = Page.step_tests.through

class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'is_child',)
    exclude = ('testable_elements',)
    # inlines = [
    #     SequenceInline,
    #     StepTestInline,
    # ]
    #exclude = ('sequence_tests','step_tests',)

    def save_model(self, request, obj, form, change):
        """ Here is where we will process the testable_elements
        in our page and then remove them from the fieldset"""
        if 'testable_elements' in request.POST:
            obj.reset_test_elements()
            # process the testable elements
            for e in request.POST.get('testable_elements').split(','):
                if e:
                    obj.add_test_element(e)

        return super(PageAdmin,self).save_model(request, obj, form, change)

    def get_urls(self):
        urls = super(PageAdmin, self).get_urls()
        host_admin_urls = patterns('',
            url(r'^sitemap/import/$', self.admin_site.admin_view(admin_sitemap_import), name='page.admin_sitemap_import',),
        )

        return host_admin_urls + urls

admin.site.register(Page, PageAdmin)
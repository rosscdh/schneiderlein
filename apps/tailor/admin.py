# -*- coding: UTF-8 -*-
from django.contrib import admin
from django.conf.urls.defaults import *
from models import CuttingRoomLog

class CuttingRoomLogAdmin(admin.ModelAdmin):
  search_fields = ['page__url']
  list_display = ('page', 'date_start', 'build_status',)
  list_filter = ('build_status',)

admin.site.register(CuttingRoomLog, CuttingRoomLogAdmin)
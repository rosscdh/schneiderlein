from django.contrib import admin
from django.conf.urls.defaults import *
from models import Sequence, SequenceTest

class SequenceTestInline(admin.TabularInline):
    model = Sequence.tests.through


class SequenceAdmin(admin.ModelAdmin):
    inlines = [
        SequenceTestInline,
    ]
    exclude = ('tests',)

admin.site.register(Sequence, SequenceAdmin)

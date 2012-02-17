from django.contrib import admin
from django.conf.urls.defaults import *
from models import Sequence, TestStep, StepTemplate

class TestStepInline(admin.TabularInline):
    model = Sequence.tests.through


class SequenceAdmin(admin.ModelAdmin):
    inlines = [
        TestStepInline,
    ]
    exclude = ('tests',)

admin.site.register(Sequence, SequenceAdmin)
admin.site.register([TestStep, StepTemplate])

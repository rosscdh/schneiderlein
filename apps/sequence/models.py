from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class StepTemplate(models.Model):
    """ Provides lettuce step template, which is to provide a list
    to the user and allow them to select template steps """
    name = models.CharField(max_length=128, blank=False)
    body = models.TextField(verbose_name=_('Step Code'), help_text=_('Lettuce Step Syntax'), blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Step Template')
        verbose_name_plural = _('Step Templates')

    def __unicode__(self):
        return '%s' % (self.name,)

class TestStep(MPTTModel):
    """ Provides a set of features to run using lettuce, makes use of the StepTemplates to define its Steps"""
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=128, blank=False)
    body = models.TextField(verbose_name=_('Test Code'), help_text=_('Cucumber/Selenium test steps'), blank=True,null=True)
    is_active = models.BooleanField(default=True)

    objects = tree = TreeManager()
    step_templates = StepTemplate.objects

    class Meta:
        verbose_name = _('Step')
        verbose_name_plural = _('Steps')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return '%s' % (self.name,)


class Sequence(MPTTModel):
    """ Provides the user with the ability to apply multiple steps to their test """
    tests = models.ManyToManyField(TestStep, related_name='sequences')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=128, blank=False)
    is_active = models.BooleanField(default=True)

    objects = tree = TreeManager()

    class Meta:
        verbose_name = _('Test Sequence')
        verbose_name_plural = _('Test Sequences')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return '%s' % (self.name,)



from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class SequenceTest(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=128, blank=False)
    body = models.TextField(verbose_name=_('Test Code'), help_text=_('Cucumber/Selenium test steps'), blank=True,null=True)
    is_active = models.BooleanField(default=True)

    objects = tree = TreeManager()

    class Meta:
        verbose_name = _('Test Step')
        verbose_name_plural = _('Test Steps')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return '%s' % (self.name,)


class Sequence(MPTTModel):
    tests = models.ManyToManyField(SequenceTest, related_name='sequences')
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


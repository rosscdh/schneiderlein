from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from apps.sequence.models import Sequence

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class Page(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    url = models.URLField()
    slug = models.SlugField()
    test_sequences = models.BooleanField(default=True)
    test_layout = models.BooleanField(default=True)
    test_layout_elements = TaggableManager()
    sequence_tests = models.ManyToManyField(Sequence, related_name='pages')

    objects = tree = TreeManager()

    class MPTTMeta:
        order_insertion_by = ['url']

    def __unicode__(self):
        return '%s' % (self.url,)

    @property
    def is_parent(self):
        return True if self.parent is None else False

    @property
    def is_child(self):
        return True if self.parent is not None else False


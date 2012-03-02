from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from apps.sequence.models import Sequence, TestStep

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager

from fields import JsonListField


class Page(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    url = models.URLField()
    slug = models.SlugField()
    testable_elements = JsonListField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

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

    def get_test_elements(self):
        if not self.testable_elements or not 'elements' in self.testable_elements:
            return None
        else:
            return self.testable_elements['elements']

    def reset_test_elements(self):
        self.testable_elements = None
        return self.testable_elements

    def add_test_element(self,value):
        if not self.testable_elements or not 'elements' in self.testable_elements:
            self.testable_elements = dict({'elements':[]})

        if value not in self.testable_elements['elements']:
            self.testable_elements['elements'].append(value)

        return self.testable_elements['elements']

    def del_test_element(self,value):
        if 'elements' in self.testable_elements:
            if value in self.testable_elements['elements']:
                self.testable_elements['elements'].remove(value)

        return self.testable_elements['elements']

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

from mptt.models import MPTTModel, TreeForeignKey

class Page(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    url = models.URLField()
    slug = models.SlugField()
    test_elements = TaggableManager()


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

class LoginPage(Page):
    username = models.CharField(max_length=128)
    username_element = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    password_element = models.CharField(max_length=128)



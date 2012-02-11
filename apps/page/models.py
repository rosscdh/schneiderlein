from django.db import models
from treebeard.mp_tree import MP_Node
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager


class Page(MP_Node):
    url = models.URLField()
    slug = models.SlugField()
    test_elements = TaggableManager()

    node_order_by = ['url']


class LoginPage(Page):
    username = models.CharField(max_length=128)
    username_element = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    password_element = models.CharField(max_length=128)


    
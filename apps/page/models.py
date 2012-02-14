from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager

import categories


class Page(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    url = models.URLField()
    slug = models.SlugField()
    test_elements = TaggableManager()
categories.register_fk(Page)


class LoginPage(Page):
    username = models.CharField(max_length=128)
    username_element = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    password_element = models.CharField(max_length=128)



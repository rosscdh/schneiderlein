import os
from django import forms
from django.core.urlresolvers import reverse


class ImportSitemapUrlForm(forms.Form):
    sitemap_url = forms.URLField(label='Sitemap Url', help_text='Enter the url to a sitemap.xml file', max_length=255)

class ImportSitemapFileForm(forms.Form):
    path = '/tmp/'
    filename = 'sitemap.xml'

    sitemap_file = forms.FileField(label='Sitemap File', help_text='Select an sitemap.xml file to upload')

    def handle_uploaded_file(self, uploaded_file):
        destination = open(os.path.join(self.path, self.filename), 'wb+')
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
        destination.close()

    def get_sitemap_local_path(self):
        return '%s%s' % (self.path, self.filename,)

    def get_absolute_url(self):
        return reverse('page-sitemap_upload', kwargs={'path': 'sitemap.xml'})

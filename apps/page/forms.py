from django import forms


class ImportSitemapUrlForm(forms.Form):
    sitemap_url = forms.URLField(label='Sitemap Url', help_text='Enter the url to a sitemap.xml file', max_length=255)

class ImportSitemapFileForm(forms.Form):
    sitemap_file = forms.FileField(label='Sitemap File', help_text='Select an sitemap.xml file to upload')

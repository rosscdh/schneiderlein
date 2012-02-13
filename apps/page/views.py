from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from forms import ImportSitemapUrlForm, ImportSitemapFileForm

@login_required
def admin_sitemap_import(request):
    import sitemap

    form_sitemapurl = ImportSitemapUrlForm()
    form_sitemapfile = ImportSitemapFileForm()

    if request.method == 'POST':
        if request.POST.get('sitemap_url', None) is not None:
            form = ImportSitemapUrlForm(request.POST)
            if form.is_valid():
                urls = sitemap.UrlSet.from_url(form.cleaned_data['sitemap_url'])

        if request.POST.get('sitemap_file', None) is not None:
            form = ImportSitemapFileForm(request.POST)
            urls = []

        if form and form.is_valid():

            for url in urls:
                print url
            assert False

    return render_to_response(
        'admin/page/sitemap_import.html', {
          'is_ajax': request.is_ajax,
          'form_sitemapurl': form_sitemapurl,
          'form_sitemapfile': form_sitemapfile,
      },
      context_instance=RequestContext(request)
    )

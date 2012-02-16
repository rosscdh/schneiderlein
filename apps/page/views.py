from django.conf import settings
from django.contrib import admin
from django.utils.encoding import smart_unicode
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from models import Page

from forms import ImportSitemapUrlForm, ImportSitemapFileForm
from util import Sitemap

import urllib2
import urlparse


@login_required
def admin_sitemap_import(request):

    UploadedSiteMap = None
    form_sitemapurl = ImportSitemapUrlForm()
    form_sitemapfile = ImportSitemapFileForm()

    if request.method == 'POST':
        if request.POST.get('sitemap_url', None) is not None:
            form = ImportSitemapUrlForm(request.POST)
            if form.is_valid():
                UploadedSiteMap = Sitemap(form.cleaned_data['sitemap_url'])

        if request.FILES.get('sitemap_file', None) is not None:
            form = ImportSitemapFileForm(request.POST, request.FILES)
            if form.is_valid():
                form.handle_uploaded_file(request.FILES['sitemap_file'])
                #local_sitemap_url = '%s%s%s' % ('http://' if not request.is_secure() else 'https://', request.get_host(), form.get_absolute_url(), )
                UploadedSiteMap = Sitemap('/tmp/sitemap.xml')

        if UploadedSiteMap is not None:
            UploadedSiteMap.get_set_pages()
            return HttpResponseRedirect( reverse('admin:page_page_changelist') )

    return render_to_response(
        'admin/page/sitemap_import.html', {
          'is_ajax': request.is_ajax,
          'form_sitemapurl': form_sitemapurl,
          'form_sitemapfile': form_sitemapfile,
      },
      context_instance=RequestContext(request)
    )

@login_required
def admin_load_page_url(request, page_id):

    page = get_object_or_404(Page, pk=page_id)
    try:
        response = urllib2.urlopen(page.url)
    except urllib2.URLError:
        raise Http404('Url "%s" is not available. Please check internet connection' % page.url)

    url = urlparse.urlparse(page.url)
    remote_html = smart_unicode(response.read())
    replace = '="%s://%s/' % (url.scheme,url.hostname,)
    remote_html = remote_html.replace('="/', replace)

    return render_to_response(
        'admin/page/page/remote_page.html', {
          'is_ajax': request.is_ajax,
          'remote_html': remote_html,
      },
      context_instance=RequestContext(request)
    )
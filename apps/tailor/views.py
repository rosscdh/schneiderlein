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
from django.core.management import call_command


@login_required
def start_process(request, process_name):

    if process_name == 'tailor_run_layout_test':
        all_pages = True if 'all_pages' in request.GET else False
        generate_screenshot = True if 'generate' in request.GET else False
        page_id = request.GET.get('page_id', None)
        if not page_id and not all_pages:
            raise Http404(unicode(_('Please specify at least 1 page_id')))

        call_command('tailor_run_layout_test', str(page_id), generate=str(generate_screenshot), all=all_pages)

    return render_to_response(
        'admin/tailor/process_log.html', {
          'is_ajax': request.is_ajax,
      },
      context_instance=RequestContext(request)
    )
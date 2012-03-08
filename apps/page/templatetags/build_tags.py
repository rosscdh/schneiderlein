from django import template
from apps.tailor.models import CuttingRoomLog

register = template.Library()


@register.inclusion_tag('page/build_results.html')
def builds_for(page):
    result_list = CuttingRoomLog.objects.filter(page=page).all()
    return dict({
        'result_list': result_list,
        'page': page,
    })

from django import template

register = template.Library()


@register.inclusion_tag('results.html')
def testelement_li(css_xpath):
    
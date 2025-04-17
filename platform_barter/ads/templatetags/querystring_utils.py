from django import template
from urllib.parse import urlencode


register = template.Library()

@register.simple_tag(takes_context=True)
def update_query(context, key, value):
    request = context['request']
    query = request.GET.copy()
    query[key] = value
    return '?' + urlencode(query)

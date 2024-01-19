# hx_request_filter.py
from django import template

register = template.Library()

@register.filter(name='is_hx_request')
def is_hx_request(request):
    return request.headers.get('hx-request') != 'true'

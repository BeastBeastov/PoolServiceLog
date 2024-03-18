from django import template
from poolservice.models import *


register = template.Library()


@register.simple_tag()
def get_pools():
    return Pool.objects.all()


@register.simple_tag(name='getlogs')
def get_logs():
    return PoolService.objects.all()

@register.simple_tag()
def get_dot(ph):
    if not ph:
        ph = '0'
    return float(str(ph).replace(',','.'))


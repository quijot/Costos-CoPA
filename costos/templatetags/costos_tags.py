from django import template

from costos.models import ParametroGlobal

register = template.Library()


@register.simple_tag
def get_cotizacion_dolar():
    return ParametroGlobal.objects.last().cotizacion_dolar


@register.simple_tag
def get_fecha():
    return ParametroGlobal.objects.last().modified.date()

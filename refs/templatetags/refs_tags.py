from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag()
def ref_html(ref, authors_nmax=None, pk=True):
    return format_html(ref.html(pk, authors_nmax))

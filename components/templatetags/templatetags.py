from django.template import Library

register = Library()


@register.simple_tag
def auto_load_ui():
    return "{% load ui_components %}"

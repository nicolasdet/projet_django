from django import template

register = template.Library()


@register.filter
def to_and(value):
    if isinstance(value, (list,)):
        return value
    return value.replace(" ", ", ")

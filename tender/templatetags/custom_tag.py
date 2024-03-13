from django import template

register = template.Library()


@register.filter
def value_from_model(model, field):
    return getattr(model, field)

@register.filter(name='capitalize_under')
def capitalize_under(value):
    value = value.replace('_', ' ')
    return value.title()
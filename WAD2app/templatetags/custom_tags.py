from django import template

register = template.Library()

@register.filter
def get_fields(obj):
    data = []
    for field in obj._meta.fields:
        val = obj._get_FIELD_display(field)
        data.append((field.name,val))
    return data

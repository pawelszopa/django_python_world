from django import template

register = template.Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
    # w templatkach to standard ze w momencie kiedy cos sie ma  wysypac to robimy cos zeby sie nie wysypal wiec retuyrn none
from django import template

register = template.Library()


@register.filter
def percentage(string, arg):
    try:
        if string:
            return string % arg
        else:
            return u''
    except (ValueError, TypeError):
        return u''


@register.filter
def js_float(float_):
    try:
        return str(float_).replace(',', '.')
    except (ValueError, TypeError):
        return '0.0'


@register.filter
def as_dict(dict_, key):
    try:
        return dict_[key]
    except (ValueError, TypeError):
        return None
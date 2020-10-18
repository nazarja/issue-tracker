from django import template

register = template.Library()


@register.filter()
def class_name(value):
    """
    This template tag function returns the name of the
    currently looped over model from a list of multiple
    model objects.
    """
    return value.__class__.__name__

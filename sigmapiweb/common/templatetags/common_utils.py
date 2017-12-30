"""
Utility functions available to all SigmaPi templates.
"""

from django import template
import os

from ..utils import get_full_name_or_deleted


register = template.Library()


@register.filter
def full_name(model, user_field_name):
    """
    Safely get the full name of user field on a model.

    Arguments:
        model (django.models.Model)
        user_field_name (str): Name of user field on model

    Returns: str
        Either the full name, or '[deleted]' if the user is None
        or not a field on model.
    """
    return get_full_name_or_deleted(
        getattr(model, user_field_name, None)
    )


@register.filter
def lookup(dictionary, key):
    """
    Lookup a key in a dictionary or list.

    Arguments:
        dictionary (dict|list)
        key (str|int)

    Returns: object
    """
    return dictionary[key]


@register.filter
def prepend(str1, str2):
    """
    Prepend the second string on the first.

    Arguments:
        str1 (str)
        str2 (str)

    Returns: str
    """
    return str2 + str1


@register.filter
def filename(path):
    """
    Return only the filename from an arbitrary path
    
    Arguments:
        path (str)
    """
    return os.path.split(path)[1]

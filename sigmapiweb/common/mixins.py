"""
General utility mixins to be used across project.
"""


class ModelMixin:
    """
    Generic mixin to be used on all models in project.
    """
    # pylint: disable=too-few-public-methods
    # Optionally override these in subclass
    admin_display_excluded_fields = ('id',)
    admin_search_fields = ()
    admin_form = None

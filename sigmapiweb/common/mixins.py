"""
General utility mixins to be used across project.
"""

class ModelMixin(object):
    """
    Generic mixin to be used on all models in project.
    """
    # Optionally override in subclass
    admin_display_excluded_fields = ('id',)

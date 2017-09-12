"""
General utility functions to be used across project.
"""
from django.contrib import admin


DELETED_STRING = '[deleted]'
NONE_SENTINEL_ID = -1


def register_model_admins(*model_classes):
    """
    Register a model with the admin site with a default list display.

    The default list display is specified by setting
    `admin_display_fields` on the model class.

    Arguments:
        *model_classes (list[class]): A class that inherits from
            common.mixins.ModelMixin
    """
    for model_class in model_classes:
        display_fields = [
            field.name
            for field in model_class._meta.fields
            if field.name not in model_class.admin_display_excluded_fields
        ]
        model_admin_class = type(
            model_class.__name__ + 'Admin',
            (admin.ModelAdmin,),
            {'list_display': tuple(display_fields)},
        )
        admin.site.register(model_class, model_admin_class)


def get_full_name_or_deleted(user):
    """
    Gets full name of a user, or [deleted] if None.

    Arguments:
        user (User)

    Returns: str
    """
    return (
        user.get_full_name()
        if user
        else DELETED_STRING
    )


def get_formal_name_or_deleted(user):
    """
    Gets "formal" name of a user ("last, first"), or [deleted] if None.

    Arguments:
        user (User)

    Returns: str
    """
    return (
        '{0}, {1}'.format(user.last_name, user.first_name)
        if user
        else DELETED_STRING
    )


def get_id_or_sentinel(model):
    """
    Gets the ID of a model, or -1 if it is None.

    Arguments:
        model (Model)

    Returns: int
    """
    return model.id if model else NONE_SENTINEL_ID


def get_user_email(user):
    """
    Gets the email for a user, falling back to default.

    Arguments:
        user (User)

    Returns: str
    """
    return user.email or get_default_email(user.username)


def get_default_email(username):
    """
    Gets default email for a username.

    Arguments:
        username (str)

    Returns: str
    """
    return username + '@wpi.edu'

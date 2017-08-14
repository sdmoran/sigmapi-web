"""
General utility functions to be used across the sigmapi-web project.
"""


DELETED_STRING = '[deleted]'
NONE_SENTINEL_ID = -1


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

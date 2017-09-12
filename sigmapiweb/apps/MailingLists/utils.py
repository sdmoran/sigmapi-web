"""
Utility functions for MailingList app.
"""


def can_user_access_mailing_list(mailing_list, user):
    """
    Check a user's permissions with respect to a mailing list.

    Arguments:
        mailing_list (MailingList)
        user (User)

    Returns: bool, bool
        Whether the user can receive and send invite,
        respectively, to the mailing list.
    """
    if user.is_staff:
        return True, True
    else:
        accesses = mailing_list.mailinglistaccess_set.all()
        groups = set(access.group for access in accesses)
        intersection = set(user.groups.all()) & groups
        receive_access = bool(intersection)
        accesses_intersection = (
            access
            for access in accesses
            if access.group in intersection
        )
        send_access = any(access.can_send for access in accesses_intersection)
        return receive_access, send_access

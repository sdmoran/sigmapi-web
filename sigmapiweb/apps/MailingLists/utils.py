"""
Utility functions for MailingList app.
"""


def can_user_access_calendar(calendar, user):
    """
    Check a user's permissions with respect to a calendar.

    Arguments:
        calendar (Calendar)
        user (User)

    Returns: bool, bool
        Whether the user can receive and send invite,
        respectively, to the calendar.
    """
    if user.is_staff:
        return True, True
    else:
        accesses = calendar.calendaraccess_set.all()
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

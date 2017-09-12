"""
Function(s) for checking access to mailing lists.
"""
from apps.UserInfo.models import PledgeClass, UserInfo

from .access_constants import ACCESS_DICT


def user_can_access_mailing_list(user, mailing_list, access_type):
    """
    Check whether a user has a certain type of access to mailing list.

    A user has access of the given type iff they have access based
    on group membership, pledge class, OR class year. Any of them suffice.

    Arguments:
        user (User)
        mailing_list (MailingList)
        access_type (str): Must be in ACCESS_DICT.keys()

    Returns: bool
    """
    if access_type not in ACCESS_DICT.keys():
        raise ValueError('Invalid access type: ' + access_type)
    if user.is_staff:
        return True

    # Check group access
    groups = frozenset(
        access.group
        for access
        in mailing_list.groupmailinglistaccess_set.filter(
            access_type=access_type
        )
    )
    if frozenset(user.groups.all()) & groups:
        return True

    # Load UserInfo
    try:
        user_info = UserInfo.objects.get(user=user)
    except UserInfo.DoesNotExist:
        # If user doesn't have group access or UserInfo, deny access
        return False

    # Check pledge class access
    pledge_classes = frozenset(
        access.pledge_class
        for access
        in mailing_list.pledgeclassmailinglistaccess_set.filter(
            access_type=access_type
        )
    )
    if user_info.pledgeClass in pledge_classes:
        return True

    # Check class year access
    class_years = frozenset(
        access.class_year
        for access
        in mailing_list.classyearmailinglistaccess_set.filter(
            access_type=access_type
        )
    )
    if user_info.graduationYear in pledge_classes:
        return True

    # Access denied
    return False

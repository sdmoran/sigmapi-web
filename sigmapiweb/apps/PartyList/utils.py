"""
Utility functions and classes for use within the PartyList modules.
"""


def check_bad_guest_list(list_cls, match_str):
    """
    Check if a guest matching the query string is on the {black|grey}list.

    Arguments:
        list_cls (type): Either BlacklistedGuest or GreylistedGuest
        match_str (str): Name of person to check {black|grey}list for

    Returns:
        (BlacklistedGuest|NoneType): The best match, or None
    """
    best_match_strength = 0
    best_match = None
    for entry in list_cls.objects.all():
        match_strength = entry.check_match(match_str)
        if match_strength > best_match_strength:
            best_match = entry
    return best_match

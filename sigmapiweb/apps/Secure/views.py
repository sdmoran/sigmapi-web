"""
Views for Secure app.
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render

from .models import CalendarKey


@login_required
def index(request):
    """
    View for the index landing page of the site.
    """

    context = {
        'title': 'Sigma Pi - Secure',
        'secure_index': True,
        # 'calendar_name_url_pairs': get_name_url_pairs(request),
    }

    return render(request, 'calendar/view.html', context)


def get_name_url_pairs(request):
    """
    Return a list of (group name, group calendar URL) pairs.

    Make sure that the Brothers or Pledges pair is last in the list, because
    the embedded calendar is set to the URL from the last pair in the list,
    and we want office positions' calendars to show up with priority over
    the general Brothers/Pledges calendar.

    Returns: (str, str)
    """
    def append_pair(pairs, group):
        """
        Given a list of (group name, group calendar URL) pairs and a group,
        if there is a calendar key for the group, add to the list.
        """
        url_template = 'https://teamup.com/%s?view=l&sidepanel=c'
        try:
            cal_key = CalendarKey.objects.get(group=group)
            pairs.append((group.name, url_template % cal_key.key))
            return True
        except CalendarKey.DoesNotExist:
            pass
        return False

    # Collect a list of (group name, group calendar URL) pairs from all groups
    #   excluding Brothers and Pledges
    name_url_pairs = []
    for group in request.user.groups.all():
        if group.name not in ['Brothers', 'Pledges']:
            append_pair(name_url_pairs, group)

    # If the user is in the Brothers or Pledges group, add the corresponding
    # key to the list
    try:
        bros_group = request.user.groups.get(name='Brothers')
    except Group.DoesNotExist:
        bros_group = None
    try:
        pledges_group = request.user.groups.get(name='Pledges')
    except Group.DoesNotExist:
        pledges_group = None
    if not (bros_group and append_pair(name_url_pairs, bros_group)):
        if pledges_group:
            append_pair(name_url_pairs, pledges_group)

    return name_url_pairs

"""
Views for Calendar app.
"""
from django.contrib.auth.models import Group
from django.shortcuts import render

from .models import Calendar, CalendarAccess, CalendarSubscription


def manage_subscriptions(request):
    """
    TODO docstring
    """
    context_calendars = []
    user_groups = set(request.user.groups.all())
    for calendar in Calendar.objects.all():
        if not request.user.is_staff:
            groups = set(
                access.group for access in calendar.calendaraccess_set.all()
            )
            if not (user_groups | groups):
                continue

        subscribed = bool(
            CalendarSubscription.objects.filter(
                calendar=calendar,
                user=request.user,
            ).count()
        )
        context_calendars.append({
            'name': calendar.name,
            'description': calendar.description,
            'subscribed': subscribed,

        })
    context = {'calendars': context_calendars}
    print(context)
    return render(request, 'calendar/manage_subscriptions.html', context)



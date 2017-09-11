"""
Views for Calendar app.
"""
from django.contrib.auth.models import Group
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .models import Calendar, CalendarAccess, CalendarSubscription


def manage_subscriptions(request):
    """
    TODO docstring
    """
    context_calendars = []
    user_groups = set(request.user.groups.all())
    for calendar in Calendar.objects.all():
        receive_access, send_access = _can_receive_and_send(
            calendar,
            request.user,
        )
        if not receive_access:
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
            'can_send': send_access,
            'subscribed': subscribed,

        })
    context = {'calendars': context_calendars}
    print(context)
    return render(request, 'calendar/manage_subscriptions.html', context)


def subscribe(request, calendar_name):
    """
    TODO docstring
    """
    if not (calendar_name and isinstance(calendar_name, str)):
        return HttpResponse(
            'Request missing \'calendar_name\' parameter',
            status_code=422,
        )
    try:
        calendar = Calendar.objects.get(name=calendar_name.lower())
    except Calendar.DoesNotExist:
        raise Http404('Calendar not found: ' + calendar_name)
    receive_access, _ = _can_receive_and_send(calendar, request.user)
    if not receive_access:
        return HttpResponse(
            'User ' + request.user.username + ' cannot access calendar ' +
            calendar.name
        )
    subscription = CalendarSubscription(
        calendar=calendar,
        user=request.user,
    )
    subscription.save()
    return redirect('calendar-manage_subscriptions')


def unsubscribe(request, calendar_name):
    """
    TODO docstring
    """
    if not (calendar_name and isinstance(calendar_name, str)):
        return HttpResponse(
            'Request missing \'calendar_name\' parameter',
            status_code=422
        )
    try:
        calendar = Calendar.objects.get(name=calendar_name.lower())
    except Calendar.DoesNotExist:
        raise Http404('Calendar not found: ' + name)
    try:
        subscription = CalendarSubscription.objects.get(
            calendar=calendar,
            user=request.user,
        )
    except CalendarSubscription.DoesNotExist:
        raise Http404(
            'User ' + request.user.username +
            ' not subscribed to ' + calendar.name
        )
    subscription.delete()
    return redirect('calendar-manage_subscriptions')


def _can_receive_and_send(calendar, user):
    """
    TODO docstring
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
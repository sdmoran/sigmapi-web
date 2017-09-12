"""
Views for MailingList app.
"""
from django.contrib.auth.models import Group
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .models import Calendar, CalendarAccess, CalendarSubscription
from .utils import can_user_access_calendar


def manage_subscriptions(request):
    """
    A view for users to see all calendars they have access to
    and subscribe/unsubscribe from them.
    """
    context_calendars = []
    user_groups = set(request.user.groups.all())
    for calendar in Calendar.objects.all():
        receive_access, send_access = can_user_access_calendar(
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
    return render(request, 'calendar/manage_subscriptions.html', context)


def set_subscribed(request, calendar_name):
    """
    POST endpoint for subscribing the logged-in user to a calendar.
    """

    # Validate request
    if request.method != 'POST':
        return HttpResponse('Only POST method allowed', status=405)
    subscribe = request.POST.get('subscribe') == 'on'
    if not (calendar_name and isinstance(calendar_name, str)):
        return HttpResponse(
            'Request missing \'calendar_name\' parameter',
            status_code=422,
        )

    # Load calendar; if subscribing, see if we have access
    try:
        calendar = Calendar.objects.get(name=calendar_name.lower())
    except Calendar.DoesNotExist:
        raise Http404('Calendar not found: ' + calendar_name)
    if subscribe:
        receive_access, _ = can_user_access_calendar(calendar, request.user)
        if not receive_access:
            return HttpResponse(
                'User ' + request.user.username + ' cannot access calendar ' +
                calendar.name
            )

    # Modify subscription
    if subscribe:
        try:
            subscription = CalendarSubscription(
                calendar=calendar,
                user=request.user,
            )
            subscription.save()
        except CalendarSubscription.IntegrityError:
            pass # No problem if we're already subscribed
    else:
        try:
            CalendarSubscription.objects.get(
                calendar=calendar,
                user=request.user,
            ).delete()
        except CalendarSubscription.DoesNotExist:
            pass  # No problem if we're not subscribed

    # Redirect to manage subscriptions page
    return redirect('calendar-manage_subscriptions')

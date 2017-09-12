"""
Views for MailingList app.
"""
from django.contrib.auth.models import Group
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from .models import MailingList, MailingListAccess, MailingListSubscription
from .utils import can_user_access_mailing_list


def manage_subscriptions(request):
    """
    A view for users to see all mailing lists they have access to
    and subscribe/unsubscribe from them.
    """
    context_mailing_lists = []
    user_groups = set(request.user.groups.all())
    for mailing_list in MailingList.objects.all().order_by('name'):
        receive_access, send_access = can_user_access_mailing_list(
            mailing_list,
            request.user,
        )
        if not receive_access:
            continue
        subscribed = bool(
            MailingListSubscription.objects.filter(
                mailing_list=mailing_list,
                user=request.user,
            ).count()
        )
        context_mailing_lists.append({
            'name': mailing_list.name,
            'description': mailing_list.description,
            'can_send': send_access,
            'subscribed': subscribed,

        })
    context = {'mailing_lists': context_mailing_lists}
    return render(request, 'mailinglists/manage_subscriptions.html', context)


def set_subscribed(request, mailing_list_name):
    """
    POST endpoint for subscribing the logged-in user to a mailing list.
    """

    # Validate request
    if request.method != 'POST':
        return HttpResponse('Only POST method allowed', status=405)
    subscribe = request.POST.get('subscribe') == 'on'
    if not (mailing_list_name and isinstance(mailing_list_name, str)):
        return HttpResponse(
            'Request missing \'mailing_list_name\' parameter',
            status_code=422,
        )

    # Load mailing list; if subscribing, see if we have access
    try:
        mailing_list = MailingList.objects.get(name=mailing_list_name.lower())
    except MailingList.DoesNotExist:
        raise Http404('MailingList not found: ' + mailing_list_name)
    if subscribe:
        receive_access, _ = can_user_access_mailing_list(
            mailing_list, request.user,
        )
        if not receive_access:
            return HttpResponse(
                'User ' + request.user.username +
                ' cannot access mailing list ' + mailing_list.name
            )

    # Modify subscription
    if subscribe:
        try:
            subscription = MailingListSubscription(
                mailing_list=mailing_list,
                user=request.user,
            )
            subscription.save()
        except MailingListSubscription.IntegrityError:
            pass # No problem if we're already subscribed
    else:
        try:
            MailingListSubscription.objects.get(
                mailing_list=mailing_list,
                user=request.user,
            ).delete()
        except MailingListSubscription.DoesNotExist:
            pass  # No problem if we're not subscribed

    # Redirect to manage subscriptions page
    return redirect('mailinglists-manage_subscriptions')

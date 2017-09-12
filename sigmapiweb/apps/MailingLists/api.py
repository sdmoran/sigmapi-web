"""
API for MailingList invites.
"""
from email import message_from_string
from email.utils import getaddresses
from smtplib import SMTP, SMTPException

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.UserInfo.models import UserInfo

from .models import MailingList, MailingListSubscription


@csrf_exempt
def send_mail(request):
    """
    TODO docstring
    """
    # Validate request
    if request.method != 'POST':
        return HttpResponse(
            'Only POST method allowed',
            status=405,
        )
    key = request.POST.get('key')
    if key != settings.MAILING_LISTS_EMAIL_API_KEY:
        return HttpResponse('Invalid API key.', status=401)

    # Parse email
    email_data = request.POST.get('data')
    if not (email_data and isinstance(email_data, str)):
        return HttpResponse(
            '\'data\' parameter missing, empty, or not a string',
            status=422,
        )
    email = message_from_string(email_data)
    addr_headers = frozenset(['from', 'to', 'resent-to', 'cc', 'resent-cc'])
    try:
        addrs_by_header = {
            header: set(
                pair[1] for pair in getaddresses(msg.get_all(header, []))
            )
            for header in addr_headers
        }
    except Exception:  # pylint: disable=broad-except
        return HttpResponse('Failed to parse from/to/cc fields', status=422)

    # Extract from address and user
    from_addrs = addrs_by_header['from']
    if not (from_addrs and len(from_addrs) == 1):
        return HttpResponse('Expected exactly one From address', status=422)
    from_addr = from_addrs[0]
    try:
        user = User.objects.get(email=from_email.lower())
    except User.DoesNotExist:
        raise Http404(
            'User with email \'{0}\' does not exist.'.format(from_email)
        )

    # Filter out addresses not in our domain; remove @domain part of addrs
    list_names_by_header = {
        header: frozenset(
            addr.split('@')
            for addr in addrs_dict[header]
            if addr.lower().endswith(
                '@' + settings.MAILING_LISTS_EMAIL_DOMAIN
            )
        )
        for header in addr_headers - {'from'}
    }

    # Turn list names into mailing lists; throw away ones that are
    # invalid or the user doesn't have send access to
    mailing_lists_by_header = {}
    for header in list_names_by_header.keys():
        mailing_lists_by_header[header] = set()
        for list_name in list_names_by_header[addr]:
            try:
                mailing_list = MailingList.objects.get(name=list_name.lower())
            except MailingList.DoesNotExist:
                continue  # Throw out non-existent mailing list
            can_send = user_can_access_mailing_list(
                user, mailing_list, ACCESS_SEND,
            )
            if not can_send:
                continue
            mailing_lists_by_header[header].add(mailing_list)

    # Expand mailing lists into their subscribers' email addresses
    new_addrs_by_header = {
        header: frozenset.union(
            (
                subscriber.email
                for subscriber in mailing_list.mailinglistsubscription_set
                if subscriber.email
            )
            for mailing_list in mailing_lists
        )
        for header, mailing_lists in mailing_lists_by_header.items()
    }

    # If we have no To addresses, return 400
    if not new_addrs_by_header['to']:
        return HttpResponse('No addresses to send mail to', status=400)

    # Turn address sets into header strings
    new_headers = {
        header: ';'.join(addrs)
        for header, addrs in new_addrs_by_header.items()
    }
    email.update(new_headers)
    email['from'] = MAILING_LISTS_FROM_EMAIL

    # Send mail
    smtp = SMTP(MAILING_LISTS_FROM_SERVER)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(MAILING_LISTS_FROM_EMAIL, MAILING_LISTS_FROM_PASSWORD)
    smtp.sendmail(
        from_addr=new_headers['from'],
        to_addrs=new_headers['to'],
        msg=email.as_string(),
    )
    smtp.quit()

    # Return 204 (Success, No Content)
    return HttpResponse('Message sent.', status=204)

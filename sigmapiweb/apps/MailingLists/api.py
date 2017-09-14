"""
API for MailingList invites.
"""
from email import message_from_string
from email.utils import getaddresses
from smtplib import SMTP, SMTPException

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from .access import user_can_access_mailing_list
from .access_constants import ACCESS_SEND
from .models import MailingList


@csrf_exempt
def send_mail(request):
    """
    View that receives raw email data and forwards it based on mailing lists.
    """
    if request.method != 'POST':
        return HttpResponse(
            'Only POST method allowed',
            status=405,
        )
    key = request.POST.get('key')
    if key != settings.MAILING_LISTS_EMAIL_API_KEY:
        return HttpResponse('Invalid API key.', status=401)
    email_data = request.POST.get('data')
    if not (email_data and isinstance(email_data, str)):
        return HttpResponse(
            '\'data\' parameter missing, empty, or not a string',
            status=422,
        )
    email = message_from_string(email_data)
    return _forward_email(email)


def _forward_email(email):
    """
    Forward email based on mailing lists.
    """
    addr_headers = frozenset(['from', 'to', 'resent-to', 'cc', 'resent-cc'])
    try:
        addrs_by_header = {
            header: set(
                pair[1] for pair in getaddresses(email.get_all(header, []))
            )
            for header in addr_headers
        }
    except Exception:  # pylint: disable=broad-except
        return HttpResponse('Failed to parse from/to/cc fields', status=422)
    from_addrs = addrs_by_header['from']
    if not (from_addrs and len(from_addrs) == 1):
        return HttpResponse('Expected exactly one From address', status=422)
    from_addr = list(from_addrs)[0]
    try:
        user = User.objects.get(email=from_addr.lower())
    except User.DoesNotExist:
        raise Http404(
            'User with email \'{0}\' does not exist.'.format(from_addr)
        )
    new_addrs_by_header = {
        header: _get_forward_addresses(addrs_by_header[header], user)
        for header in addr_headers - {'from'}
    }
    to_addrs = list(new_addrs_by_header['to'])
    if not to_addrs:
        return HttpResponse('No addresses to send mail to', status=400)
    new_headers = {
        header: ';'.join(addrs)
        for header, addrs in new_addrs_by_header.items()
    }
    for header, value in new_headers.items():
        try:
            email.replace_header(header, value)
        except KeyError:
            email[header] = value
    _strip_unwanted_headers(email)
    return _send_email(email, from_addr, to_addrs)


def _get_forward_addresses(original_addrs, user):
    """
    Given a list of email addresses, calculate who we should forward to.

    Arguments:
        original_addrs (frozenset[str])

    Returns: frozenset(str)
    """
    mailing_list_names = frozenset(
        addr.split('@')[0]
        for addr in original_addrs
        if addr.lower().endswith(
            '@' + settings.MAILING_LISTS_EMAIL_DOMAIN
        )
    )
    mailing_lists = set()
    for list_name in mailing_list_names:
        try:
            mailing_list = MailingList.objects.get(name=list_name.lower())
        except MailingList.DoesNotExist:
            continue  # Throw out non-existent mailing list
        can_send = user_can_access_mailing_list(
            user, mailing_list, ACCESS_SEND,
        )
        if not can_send:
            continue
        mailing_lists.add(mailing_list)
    return frozenset.union(frozenset(), *(
        frozenset(
            subscription.user.email
            for subscription
            in mailing_list.mailinglistsubscription_set.all()
            if subscription.user.email
        )
        for mailing_list in mailing_lists
    ))


def _strip_unwanted_headers(email):
    """
    Remove headers from the email that prevent it from being forwarded.

    Arguments:
        email (email object)
    """
    strip_header_substrings = frozenset([
        'arc-', 'return-path', 'signature', 'spam', 'x-',
        'delivered-to', 'received', 'authentication',
        'message-id',
    ])
    for key in email.keys():
        for substring in strip_header_substrings:
            if substring in key.lower():
                del email[key]
                break


def _send_email(email, from_addr, to_addrs):
    """
    Try to send an email message and return an HTTP response.

    Arguments:
        email (emailobject)
        from_addr (str)
        to_addrs(list[str])

    Returns: HttpResponse
    """
    try:
        smtp = SMTP(settings.MAILING_LISTS_FROM_SERVER)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(
            settings.MAILING_LISTS_FROM_EMAIL,
            settings.MAILING_LISTS_FROM_PASSWORD,
        )
        smtp.sendmail(
            from_addr=from_addr,
            to_addrs=to_addrs,
            msg=email.as_string(),
        )
        smtp.quit()
    except SMTPException:
        return HttpResponse(
            'An error occured while forwarding email',
            status=500,
        )
    return HttpResponse('Message sent.', status=204)

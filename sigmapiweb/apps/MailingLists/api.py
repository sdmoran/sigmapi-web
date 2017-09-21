"""
API for MailingList invites.
"""
from datetime import datetime, timedelta
from email import message_from_string
from email.mime.text import MIMEText
from email.utils import getaddresses
from smtplib import SMTP, SMTPException

from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .access import user_can_access_mailing_list
from .access_constants import ACCESS_SEND, ACCESS_SUBSCRIBE
from .models import MailingList, UserLastSentTime


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
    addrs_by_header = _get_addrs_by_header(email)
    if not addrs_by_header:
        return HttpResponse('Failed to parse headers from email.', status=422)
    from_addrs = addrs_by_header.pop('from')
    if not (from_addrs and len(from_addrs) == 1):
        return HttpResponse('Expected exactly one From address', status=422)
    from_addr = list(from_addrs)[0]
    errors, status = _forward_email(email, from_addr, addrs_by_header)
    if errors:
        _send_errors_email(
            errors,
            200 <= status <= 299,
            email.get('Subject', '[No subject]'),
            from_addr,
        )
    return HttpResponse(
        (
            "Email message successfully forwarded."
            if 200 <= status <= 299
            else "Failed to forward email message."
        ),
        status=status,
    )


def _get_addrs_by_header(email):
    """
    Parse addresses from email headers.

    Arguments:
        email (email object)

    Returns: dict[str: frozenset[str]]
    """
    addr_headers = frozenset(['from', 'to', 'resent-to', 'cc', 'resent-cc'])
    try:
        return {
            header: frozenset(
                pair[1] for pair in getaddresses(email.get_all(header, []))
            )
            for header in addr_headers
        }
    except Exception:  # pylint: disable=broad-except
        return None


def _forward_email(email, from_addr, dest_addrs_by_header):
    """
    Forward email based on mailing lists.

    Arguments:
        email (email object)
        from_addr (str)
        dest_addrs_by_header (dict[str: frozenset(str)]): Dict mapping
            destination headers to sets of addresses

    Returns: frozenset[str], int, str
        A set of errors that occured, an HTTP status code, and
        the address that the email was sent from.
    """
    try:
        user = User.objects.get(email=from_addr.lower())
    except User.DoesNotExist:
        return frozenset([
            'User with email \'{0}\' does not exist.'.format(from_addr)
        ]), 403
    if not _check_last_sent_time_constraint(user):
        return frozenset([
            'Each user can only send one email every 15 seconds.',
        ]), 429
    new_addrs_by_header = {}
    all_errors = frozenset()
    for header, orig_addrs in dest_addrs_by_header.items():
        new_addrs, errors = _get_forward_addresses(orig_addrs, user)
        new_addrs_by_header[header] = new_addrs
        all_errors = all_errors.union(errors)
    to_addrs = list(new_addrs_by_header['to'])
    if not to_addrs:
        return all_errors, 400
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
    send_errors = _send_email(email, from_addr, to_addrs)
    return (
        all_errors.union(send_errors),
        500 if send_errors else 204,
    )


def _get_forward_addresses(original_addrs, user):
    """
    Given a list of email addresses, calculate who we should forward to.

    Arguments:
        original_addrs (frozenset[str])

    Returns: frozenset(str), frozenset(str)
        A set of forward addresses and a list of errors.
    """
    mailing_list_names = frozenset(
        addr.split('@')[0]
        for addr in original_addrs
        if addr.lower().endswith(
            '@' + settings.MAILING_LISTS_EMAIL_DOMAIN
        )
    )
    mailing_lists = set()
    errors = set()
    for list_name in mailing_list_names:
        try:
            mailing_list = MailingList.objects.get(name=list_name.lower())
        except MailingList.DoesNotExist:
            errors.add("Non-existent mailing list '" + list_name + "'")
            continue  # Throw out non-existent mailing list
        can_send = user_can_access_mailing_list(
            user, mailing_list, ACCESS_SEND,
        )
        if not can_send:
            errors.add(
                "You do not have send access to the mailing list '" +
                list_name + "'"
            )
            continue
        mailing_lists.add(mailing_list)
    res_forward_addrs = frozenset.union(frozenset(), *(
        frozenset(
            subscription.user.email
            for subscription
            in mailing_list.mailinglistsubscription_set.all()
            if (
                subscription.user.email and
                user_can_access_mailing_list(
                    subscription.user, mailing_list, ACCESS_SUBSCRIBE
                )
            )
        )
        for mailing_list in mailing_lists
    ))
    res_errors = frozenset(errors)
    return res_forward_addrs, res_errors


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


def _check_last_sent_time_constraint(user):
    """
    Check if the user can send an email based on when they last sent one.

    Arguments:
        user (User)

    Returns: bool
    """
    now = datetime.now()
    try:
        last_sent_record = UserLastSentTime.objects.get(user=user)
    except UserLastSentTime.DoesNotExist:
        UserLastSentTime(user=user, last_sent=now).save()
        return True
    min_timedelta = timedelta(
        seconds=UserLastSentTime.MIN_SECONDS_BETWEEN_SENDS
    )
    can_send = now - last_sent_record.last_sent >= min_timedelta
    last_sent_record.last_sent = now
    last_sent_record.save()
    return can_send


def _send_errors_email(errors, was_sent, original_subject, to_addr):
    """
    Try to respond to the sender with a list of errors.

    Arguments:
        errors (frozenset[str])
        was_sent (bool): Whether the message was successfully sent to any list
        original_subject (str)
        to_addr (str)
    """
    if not errors:
        return
    msg = MIMEText(
        "The following errors arose while trying " +
        "to send your message entitled '" + original_subject +
        "':\n\n- " +
        "\n\n- ".join(errors) + (
            (
                "\n\nPlease note that your message was successfully sent " +
                "to mailing list(s) not shown here."
            ) if was_sent else ""
        )
    )
    msg['Subject'] = "Errors while sending to mailing list(s)"
    msg['From'] = settings.MAILING_LISTS_FROM_EMAIL
    msg['To'] = to_addr
    _send_email(msg, settings.MAILING_LISTS_FROM_EMAIL, to_addr)


def _send_email(email, from_addr, to_addrs):
    """
    Try to send an email message and return an HTTP response.

    Arguments:
        email (email object)
        from_addr (str)
        to_addrs(list[str])

    Returns: frozenset[str]
        A set of errors that occured
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
        return frozenset(['An error occured while forwarding email'])
    return frozenset()

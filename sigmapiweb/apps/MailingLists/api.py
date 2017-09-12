"""
API for MailingList invites.
"""
from email import message_from_string
from smtplib import SMTP, SMTPException

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from apps.UserInfo.models import UserInfo

from .models import MailingList, MailingListSubscription
from .utils import can_user_access_mailing_list


@csrf_exempt
def send_mail(request):
    """
    TODO docstring
    """
    if request.method != 'POST':
        return HttpResponse(
            'Only POST method allowed',
            status=405,
        )

    key = request.POST.get('key')
    if key != settings.EMAIL_API_KEY:
        return HttpResponse('Invalid API key.', status=401)
    email_data = request.POST.get('data')
    if not (email_data and isinstance(email_data, str)):
        return HttpResponse(
            '\'data\' parameter missing, empty, or not a string',
            status=422,
        )

    subject_line = None
    from_line = None
    for line in email_data.splitlines():
        if line.startswith('Subject: '):
            subject_line = line[len('Subject: '):]
        elif line.startswith('From: '):
            from_line = line[len('From: '):]
    if not (from_line and subject_line):
        return HttpResponse(
            'Data does not have Subject and/or From',
            status=422,
        )

    try:
        mailing_list = _get_mailing_list_from_subject_line(subject_line)
        user = _get_user_from_from_line(from_line)
    except RuntimeError as e:
        return HttpResponse(str(e), status=500)
    _, can_send = can_user_access_mailing_list(mailing_list, user)
    if not can_send:
        fmt = 'User \'{0}\' does not have permission to send to \'{1}\''
        return HttpResponse(
            fmt.format(user.username, mailing_list.name),
            status=403,
        )

    try:
        _forward_email(mailing_list, subject_line, email_data)
    except SMTPException:
        return HttpResponse(
            'Error occured while sending invite to \'{0}\''.format(
                mailing_list.name,
            ),
            status=500,
        )
    except ValueError:
        return HttpResponse(
            'MailingList has no subscribers',
            status=204,
        )
    return HttpResponse('Message sent.', status=204)


def _get_mailing_list_from_subject_line(subject_line):
    """
    Parse a MailingList instance out of an email subject line.

    Arguments:
        subject_line (str): Subject not including "Subject: "

    Returns: MailingList

    Raises: Http404 if MailingList does not exist
    """
    mailing_list_name = subject_line[:subject_line.index(':')]
    try:
        return MailingList.objects.get(name=mailing_list_name)
    except MailingList.DoesNotExist:
        raise Http404(
            'MailingList \'{0}\' does not exist.'.format(mailing_list_name)
        )


def _get_user_from_from_line(from_line):
    """
    Parse a User out of an email "From" line.

    Arguments:
        from_line (str): From line not including "From: "

    Returns: User

    Raises:
        Http404: if User does not exist
        RuntimeError: multiple matching Users found
    """
    start_index = from_line.index('<')
    end_index = from_line.index('>')
    if start_index < 0 or end_index < 1:
        return HttpResponse(
            'From header is malformed',
            status=422,
        )
    from_email = from_line[(start_index + 1):end_index]
    try:
        return User.objects.get(email=from_email.lower).user
    except User.DoesNotExist:
        raise Http404(
            'User with email \'{0}\' does not exist.'.format(from_email)
        )
    except MultipleObjectsReturned:
        raise RuntimeError(
            'Multiple users exist with email \'{0}\''.format(from_email)
        )


def _forward_email(mailing_list, subject, email_data):
    """
    Forward an email to all subscribers of a mailing_list.

    Arguments:
        mailing_list (MailingList)
        email_data (str)
        from_addr (str)

    Raises:
        ValueError: MailingList has no subscribers
        SMTPExcpetion: Message failed to send

    """
    from_addr = 'kylemccorspam@gmail.com'

    to_addrs = (
        sub.user.email
        for sub in MailingListSubscription.objects.filter(
            mailing_list=mailing_list
        )
    )
    email = message_from_string(email_data)
    to_addrs_joined = ';'.join(to_addrs)
    _set_header(email, 'to', to_addrs_joined)
    _set_header(email, 'from', from_addr)

    #s = SMTP('localhost')
    #s.send_message(email, from_addr=from_addr, to_addrs=to_addrs)
    #s.quit()
    #import pdb;pdb.set_trace()
    smtp = SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(from_addr, 'REDACTED')
    smtp.sendmail(from_addr, to_addrs, email.as_string())
    smtp.quit()


def _set_header(email, header, value):
    """
    TODO docstring
    """
    try:
        email.replace_header(header, value)
    except KeyError:
        email[header] = value

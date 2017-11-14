"""
Utility functions for notifying users about Standards events
"""
from django.conf import settings
from django.contrib.auth.models import User

from common.utils import send_email


def summons_requested(summons_request_count):
    """
    Get a message for a summons request.
    """
    subject = 'Standards Board: New Summons Request(s) Submitted'
    message = (
        str(summons_request_count) +
        ' new summons request(s) have been submitted for your approval. ' +
        'You may view details on the request and approve/deny it at: ' +
        'https://sigmapigammaiota.org/secure/standards/summons/requests/'
    )
    fourth = User.objects.get(groups__name='4th Counselor')
    send_email(
        subject=subject,
        body=message,
        to_emails=[fourth.email],
        cc_emails=[],
    )


def summons_request_denied(summons_request):
    """
    Get a message for a summons request denial.
    """
    subject = 'Standards Board: Summons Request Denied'
    message = (
        'Your request to summons ' +
        summons_request.summonee.first_name + ' ' +
        summons_request.summonee.last_name +
        ' has been denied. If you want more details, ' +
        'please speak with the Fourth Counselor.'
    )
    fourth = User.objects.get(groups__name='4th Counselor')
    send_email(
        subject=subject,
        body=message,
        to_emails=[summons_request.summoner.email],
        cc_emails=[fourth.email],
    )


def summons_sent(summons):
    """
    Get a message for receiving a summons.
    """
    subject = 'Standards Board: Summons'
    message = (
        'Date: ' + summons.dateSummonsSent.strftime('%Y-%m-%d') + '. ' +
        'You are receiving this email because you are being summoned by ' +
        summons.summonee.first_name + ' ' + summons.summonee.last_name + '. '
    )
    if summons.spokeWith:
        message += (
            ' The recorded outcome of your conversation with the summoner ' +
            'is: ' + summons.outcomes +
            '. The summoner has requested this case be ' +
            'sent to Standards Board for the following reason: ' +
            summons.standards_action + '. '
        )
    else:
        message += (
            'The reason for your summon is as follows: ' +
            summons.special_circumstance + '. '
        )
    message += (
        'If you feel that you are being unfairly sanctioned, ' +
        'you may attend the next Standards Board meeting to dispute ' +
        'the summon. If you do not attend, you will automatically be given ' +
        'a punishment by standards.'
    )
    fourth = User.objects.get(groups__name='4th Counselor')
    standards = User.objects.get(groups__name='Parliamentarian')
    send_email(
        subject=subject,
        body=message,
        to_emails=[summons.summonee.email],
        cc_emails=[fourth.email, standards.email, settings.EC_EMAIL],
    )

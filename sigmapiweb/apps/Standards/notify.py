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
        'https://sigmapigammaiota.org/secure/standards/summons/requests/')
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
    subject = 'Standards Board: Summons Received'

    if summons.spokeWith:
        summons_info = (
            'The recorded outcome of your '
            'conversation with the summoner is:\n\n{0}.'
            'The summoner has requested this case be '
            'sent to the Standards Board '
            'for the following reason:\n\n{1}').format(
                summons.outcomes, summons.standards_action
        )
    else:
        summons_info = (
            "The reason for your summons is as follows:"
            "\n\n{0}".format(
                summons.special_circumstance))

    message_context = {
        'date': 'Date: {0}.'.format(
            summons.dateSummonsSent.strftime('%Y-%m-%d')),
        'summoner_info': (
            'You are receiving this email because you have'
            ' been summoned by {0} {1}.'.format(
                summons.summoner.first_name,
                summons.summoner.last_name
            )
        ),
        'summons_info': summons_info,
        'outcome': (
            'Please come to the next Standards meeting, '
            'where the summons will be heard. '
            'You will have the opportunity to make your case, '
            'after which time the Standards board will decide on an action. '
            'If you cannot make the meeting, '
            'please speak with the Parliamentarian.'
        ),
    }
    message = (
        '{date}\n\n{summoner_info}\n\n'
        '{summons_info}\n\n{outcome}'.format(**message_context)
    )
    fourth = User.objects.get(groups__name='4th Counselor')
    standards = User.objects.get(groups__name='Parliamentarian')
    send_email(
        subject=subject,
        body=message,
        to_emails=[summons.summonee.email],
        cc_emails=[fourth.email, standards.email, settings.EC_EMAIL],
    )

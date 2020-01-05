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
    subject = 'Standards Board: Summoning Request Approved'

    if summons.spokeWith:
        summons_info = (
            'The recorded details of your '
            'conversation with the summoner is:\n\n\t"{0}"\n\n'
            'The summoner has requested this case be '
            'sent to the Standards Board '
            'for the following reason:\n\n\t"{1}"').format(
                summons.outcomes, summons.standards_action
        )
    else:
        summons_info = (
            "The reason for your summons is as follows:"
            "\n\n\t\"{0}\"".format(
                summons.special_circumstance))

    message_context = {
        'date': 'Date: {0}.'.format(
            summons.dateSummonsSent.strftime('%Y-%m-%d')),
        'summoner_info': (
            # This is all treated as one string, so there is only one
            # format at the end
            '{0},\n\n'
            'You are receiving this email because you have'
            ' been summoned by {1} {2}.'.format(
                summons.summonee.first_name,
                summons.summoner.first_name,
                summons.summoner.last_name
            )
        ),
        'summons_info': summons_info,
        'outcome': (
            'Please come to the next Standards meeting following your case'
            'being anounced at a house meeting. '
            'This is the meeting where you case will be heard. '
            'You will have the opportunity to make your case, '
            'after which time the Standards board will decide if an '
            'appropriate sanction should be imposed. '
            'If you cannot make the meeting for a legitimate purpose, '
            'please speak with the Parliamentarian.'
            '\n\nAs per the bylaws, chosing not to come without an excuse '
            'will be considered as an affirmation of fault and may have '
            'adverse consequences.'
        ),
    }
    message = (
        '{date}\n\n{summoner_info} '
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


def notify_outcome(summons_record):
    """
    Inform the summoned of the outcome if action was taken
    """
    subject = 'Standards Board: Action Taken'

    text = (
        "{0},\n\n"
        "In the summoning filed by {1} "
        "against you, the standards board has decided to take action. "
        "The sanction against you, as voted on by the justices, is:\n\n"
        "\t\"{2}\"\n\n"
        "If you believe that you do not deserve this sanction or that the "
        "standards board has erred, you may appeal the decision at the next "
        "house meeting during new business. If you have questions on how to "
        "appeal, or what the process will be like, "
        "please contact the Parliamentarian.".format(
            summons_record.summonee.first_name,
            summons_record.summoner.first_name,
            summons_record.resultReason,
        )
    )

    p_email = User.objects.get(groups__name='Parliamentarian').email
    send_email(
        subject=subject,
        body=text,
        to_emails=[summons_record.summonee.email],
        cc_emails=[summons_record.summoner.email, p_email],
    )

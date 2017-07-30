"""
    Utility functions for notifying users about Standards events
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage


def summons_requested(summonsRequestCount):
    subject = "Standards Board: New Summons Request(s) Submitted"
    message = str(summonsRequestCount) + " new summons request(s) have been submitted for your approval."
    message += " You may view details on the request and approve/deny it at: https://sigmapigammaiota.org/secure/standards/summons/requests/"

    try:
        fourth = User.objects.get(groups__name='4th Counselor')

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [fourth.email])
    except:
        pass


def summons_request_denied(summonsRequest):
    subject = "Standards Board: Summons Request Denied"
    message = "Your request to summons " + summonsRequest.summonee.first_name + " " + summonsRequest.summonee.last_name
    message += " has been denied. If you want more details, please speak with the Fourth Counselor."

    try:
        fourth = User.objects.get(groups__name='4th Counselor')

        email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
                             to=[summonsRequest.summoner.email], cc=[fourth.email])

        email.send()
    except:
        pass


def summons_sent(summons):
    subject = "Standards Board: Summons"
    message = "Date: " + summons.dateSummonsSent.strftime("%Y-%m-%d") + ". "
    message += "You are receiving this email because you are being summoned."
    if summons.spokeWith:
        message += " The recorded outcome of your conversation with the summonee (" + \
                   summons.summonee.last_name + ", " + summons.summonee.first_name + ") is: "
        message += summons.outcomes
        message += ". The summonee has requested this case be sent to Standards Board for the following reason: " + summons.standards_action
        message += "."
    else:
        message = message + " The reason for your summon is as follows: " + summons.special_circumstance + "."
    message += " If you feel that you are being unfairly sanctioned, you may attend the next Standards Board meeting to dispute the summon."
    message += " If you do not attend, you will automatically be given a punishment by standards."

    try:
        fourth = User.objects.get(groups__name='4th Counselor')
        standards = User.objects.get(groups__name='Parliamentarian')

        email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
                             to=[summons.summonee.email], cc=[fourth.email, standards.email, settings.EC_EMAIL])

        email.send()
    except:
        pass

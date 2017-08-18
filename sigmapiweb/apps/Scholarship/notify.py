"""
Utility functions for notifying users about Study Hours events
"""
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def scholarship_content_submitted():
    """
    TODO: Docstring
    """
    subject = "Scholarship: Content Submitted for Approval"
    message = (
        "Content has been submitted to " +
        "the Scholarship module for your approval. " +
        "You may view and approve/deny " +
        "this content at" +
        "https://sigmapigammaiota.org/secure/scholarship/approve/"
    )

    scholarship = User.objects.filter(groups__name='Scholarship Chair')
    if not scholarship.exists():
        return
    scholarship = scholarship[0]

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[scholarship.email],
        )
        email.send()
    except SMTPException:
        pass  # TODO: Do something here


def study_hours_tracked(tracked_user):
    """
    TODO: Docstring
    """
    subject = "Scholarship: Study Hours"
    message = (
        "Based on your academic performance, " +
        "you are now required to report " +
        str(tracked_user.number_of_hours) + " " +
        "study hours per week. "
        "Weeks begin on Mondays and " +
        "end at Sunday at midnight. "
        "You may report your study hours " +
        "at: https://sigmapigammaiota.org/secure/scholarship/study_hours/"
    )

    scholarship = User.objects.filter(groups__name='Scholarship Chair')
    if not scholarship.exists():
        return
    scholarship = scholarship[0]

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[tracked_user.user.email],
            cc=[scholarship.email],
        )
        email.send()
    except SMTPException:
        pass  # TODO: Do something here


def study_hours_untracked(tracked_user):
    """
    TODO: Docstring
    """
    subject = "Scholarship: Study Hours"
    message = "Based on your academic performance," +\
        " you are no longer required to report study hours."

    scholarship = User.objects.filter(groups__name='Scholarship Chair')
    if not scholarship.exists():
        return
    scholarship = scholarship[0]

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[tracked_user.user.email],
            cc=[scholarship.email],
        )
        email.send()
    except SMTPException:
        pass  # TODO: Do something here


def social_probation(tracked_user):
    """
    TODO: Docstring
    """
    subject = "Scholarship: Social Probation"
    message = "You have been placed on social probation" +\
        " for failing to complete study hours."

    scholarship = User.objects.filter(groups__name='Scholarship Chair')
    if not scholarship.exists():
        return
    scholarship = scholarship[0]

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[tracked_user.user.email],
            cc=[scholarship.email, settings.EC_EMAIL],
        )
        email.send()
    except SMTPException:
        pass  # TODO: Do something here

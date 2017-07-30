"""
    Utility functions for notifying users about Study Hours events
"""
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

def scholarship_content_submitted():
    subject = "Scholarship: Content Submitted for Approval"
    message = "Content has been submitted to the Scholarship module for your approval."
    message = message + " You may view and approve/deny this content at https://sigmapigammaiota.org/secure/scholarship/approve/"

    try:
        scholarship = User.objects.filter(groups__name='Scholarship Chair')

        if scholarship.exists():
            scholarship = scholarship[0]

            email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
                to=[scholarship.email])
            
            email.send()
    except:
        pass


def study_hours_tracked(trackedUser):
    subject = "Scholarship: Study Hours"
    message = "Based on your academic performance, you are now required to report " + str(trackedUser.number_of_hours) + " study hours per week."
    message = message + " Weeks begin on Mondays and end at Sunday at midnight."
    message = message + " You may report your study hours at: https://sigmapigammaiota.org/secure/scholarship/study_hours/"

    try:
        scholarship = User.objects.filter(groups__name='Scholarship Chair')

        if scholarship.exists():
            scholarship = scholarship[0]

            email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
                to=[trackedUser.user.email], cc=[scholarship.email])
            
            email.send()
    except:
        pass

def study_hours_untracked(trackedUser):
    subject = "Scholarship: Study Hours"
    message = "Based on your academic performance, you are no longer required to report study hours."

    try:
        scholarship = User.objects.filter(groups__name='Scholarship Chair')

        if scholarship.exists():
            scholarship = scholarship[0]

            email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
                to=[trackedUser.user.email], cc=[scholarship.email])
            
            email.send()
    except:
        pass

def social_probation(trackedUser):
    subject = "Scholarship: Social Probation"
    message = "You have been placed on social probation for failing to complete study hours."

    try:
        scholarship = User.objects.filter(groups__name='Scholarship Chair')

        if scholarship.exists():
            scholarship = scholarship[0]

            email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
                to=[trackedUser.user.email], cc=[scholarship.email, settings.EC_EMAIL])
            
            email.send()
    except:
        pass
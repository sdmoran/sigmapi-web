"""
Utility functions and classes for use within the UserInfo modules.
"""
from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import IntegrityError

from common.utils import get_default_email

from .models import UserInfo


class CreateUserError(Exception):
    """
    Exception raised by create_user.
    """
    pass


def get_senior_year():
    """
    Returns the upcoming graduation year of the current seniors.

    Returns: int
    """
    time_tuple = date.today().timetuple()
    year = time_tuple[0]
    month = time_tuple[1]
    return year + 1 if month >= 6 else year


def create_user(username, first_name, last_name, major, year):
    """
    Creates a user with the given username, populating info with web scraper.

    Arguments:
        username (str)
        first_name (str)
        last_name (str)
        major (str)
        year (int)

    Raises:
        CreateUserError: username taken, or something invalid
    """
    try:
        user_obj = User.objects.create(username=username)
    except IntegrityError:
        raise CreateUserError('Username already taken')
    except ValueError:
        raise CreateUserError('Invalid username')

    try:
        user_obj.email = get_default_email(username)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        password = User.objects.make_random_password()
        user_obj.set_password(password)

        user_info_obj = UserInfo.objects.create(user=user_obj)
        user_info_obj.major = major
        user_info_obj.graduationYear = year

        user_obj.save()
        user_info_obj.save()

        if not settings.DEBUG:
            send_mail_to_new_user(user_obj.username, user_obj.email, password)
    except (ValueError, ValidationError):
        if user_obj:
            user_obj.delete()
        raise CreateUserError('Invalid name, major, or year')


def send_mail_to_new_user(username, email, password):
    """
    Sends a notice to a new user that their account has been setup.

    Arguments:
        username (str)
        email (str)
        password (str)
    """
    subject = 'Welcome to the Sigma Pi Gamma Iota Website'
    message = (
        'Welcome to the Sigma Pi Gamma Iota website.'
        ' An account has been created for you.  Your username is: ' +
        username + '. Your password is: ' + password + '. ' +
        'You may acess the website at: https://sigmapigammaiota.org. ' +
        'It is highly reccommended that you change your password upon ' +
        'logging in.'
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


def reset_password(username):
    """
    Resets a user's password.

    Arguments:
        username (str)
    """
    user_obj = User.objects.get(username=username)

    password = User.objects.make_random_password()
    user_obj.set_password(password)
    user_obj.save()

    if not settings.DEBUG:
        send_mail_reset_password(user_obj.username, user_obj.email, password)


def send_mail_reset_password(username, email, password):
    """
    Sends a notice to a user that their password has been reset.

    Arguments:
        username (str)
        email (str)
        password (str)
    """
    subject = 'Your Password has been Reset'
    message = (
        'Your password for the Sigma Pi Gamma Iota website has been reset.' +
        ' Your username is: ' +
        username + '. Your new password is: ' + password + '. ' +
        'You may acess the website at: https://sigmapigammaiota.org. ' +
        'It is highly reccommended that you change your password upon ' +
        'logging in.'
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

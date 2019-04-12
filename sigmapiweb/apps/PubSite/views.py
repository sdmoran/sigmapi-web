"""
Views for PubSite app.
"""
from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.shortcuts import render
from django.contrib.auth.models import User


def _get_context(page_name):
    return {
        'pages': settings.PUBLIC_PAGES,
        'current_page_name': page_name,
    }


def index(request):
    """
    View for the static index page
    """
    return render(request, 'public/home.html', _get_context('Home'))


def about(request):
    """
    View for the static chapter history page.
    """
    return render(request, 'public/about.html', _get_context('About'))


def activities(request):
    """
    View for the static chapter service page.
    """
    return render(
        request,
        'public/activities.html',
        _get_context('Service & Activities'),
    )


def iqpmap(request):
    """
    View for the interactive IQP map.
    """
    iqpbrothers = User.objects.exclude(userinfo__iqpCity=None).order_by("last_name")


    context = {
        'pages': settings.PUBLIC_PAGES,
        'current_page_name': 'IQP Map',
        'brothers': iqpbrothers
    }

    return render(
        request, 'public/iqpmap.html', context,
    )

"""
def users(request):
    Provides the collections of brothers in the house.

    Organizes them based on year and exec positions.
    TODO: Refactor
    
    # pylint: disable=too-many-statements

    # Find out what current year is the senior year grad date.
    senior_year = utils.get_senior_year()

    # Get the execs.
    # Use try/catch to avoid crashing the site if an exec is missing.
    # The "newX" positions are for when NME needs the updated list for
    # notebooks, but permissions aren't transitioned yet
    # (last two weeks of B-term basically)
    sage = check_user_exists('Sage', 'newSage')
    second = check_user_exists('2nd Counselor', 'new2nd')
    third = check_user_exists('3rd Counselor', 'new3rd')
    fourth = check_user_exists('4th Counselor', 'new4th')
    first = check_user_exists('1st Counselor', 'new1st')
    herald = check_user_exists('Herald', 'newHerald')

    # Get the rest of the users.  Exclude pledges or any execs.
    seniors = User.objects.filter(groups__name='Brothers')
    seniors = seniors.filter(
        userinfo__graduationYear__lte=senior_year
    ).prefetch_related('userinfo').order_by("last_name")

    juniors = User.objects.filter(
        userinfo__graduationYear=(senior_year + 1)
    ).prefetch_related('userinfo').order_by("last_name")
    juniors = juniors.exclude(groups__name='Pledges')
    juniors = juniors.exclude(groups__name='Alumni')

    sophomores = User.objects.filter(
        userinfo__graduationYear=(senior_year + 2)
    ).prefetch_related('userinfo').order_by("last_name")
    sophomores = sophomores.exclude(groups__name='Pledges')
    sophomores = sophomores.exclude(groups__name='Alumni')

    freshmen = User.objects.filter(
        userinfo__graduationYear=(senior_year + 3)
    ).prefetch_related('userinfo').order_by("last_name")
    freshmen = freshmen.exclude(groups__name='Pledges')
    freshmen = freshmen.exclude(groups__name='Alumni')

    # Exclude the execs, if applicable.
    if sage is not None:
        seniors = seniors.exclude(username=sage.username)
        juniors = juniors.exclude(username=sage.username)
        sophomores = sophomores.exclude(username=sage.username)
        freshmen = freshmen.exclude(username=sage.username)
        sage.title = "Sage"

    if second is not None:
        seniors = seniors.exclude(username=second.username)
        juniors = juniors.exclude(username=second.username)
        sophomores = sophomores.exclude(username=second.username)
        freshmen = freshmen.exclude(username=second.username)
        second.title = "2nd Counselor"

    if third is not None:
        seniors = seniors.exclude(username=third.username)
        juniors = juniors.exclude(username=third.username)
        sophomores = sophomores.exclude(username=third.username)
        freshmen = freshmen.exclude(username=third.username)
        third.title = "3rd Counselor"

    if fourth is not None:
        seniors = seniors.exclude(username=fourth.username)
        juniors = juniors.exclude(username=fourth.username)
        sophomores = sophomores.exclude(username=fourth.username)
        freshmen = freshmen.exclude(username=fourth.username)
        fourth.title = "4th Counselor"

    if first is not None:
        seniors = seniors.exclude(username=first.username)
        juniors = juniors.exclude(username=first.username)
        sophomores = sophomores.exclude(username=first.username)
        freshmen = freshmen.exclude(username=first.username)
        first.title = "1st Counselor"

    if herald is not None:
        seniors = seniors.exclude(username=herald.username)
        juniors = juniors.exclude(username=herald.username)
        sophomores = sophomores.exclude(username=herald.username)
        freshmen = freshmen.exclude(username=herald.username)
        herald.title = "Herald"

    context = {
        'pages': settings.PUBLIC_PAGES,
        'current_page_name': 'Brothers',
        'brother_groups': [
            {
                'group_title': 'Executive Council',
                'brothers': [sage, second, third, fourth, first, herald],
                'count': 6
            },
            {
                'group_title': 'Seniors',
                'brothers': seniors,
                'count': len(seniors)
            },
            {
                'group_title': 'Juniors',
                'brothers': juniors,
                'count': len(juniors)
            },
            {
                'group_title': 'Sophomores',
                'brothers': sophomores,
                'count': len(sophomores)
            },
            {
                'group_title': 'Freshmen',
                'brothers': freshmen,
                'count': len(freshmen)
            }
        ]
    }

    return render(request, 'userinfo/public/brothers.html', context)

"""

def permission_denied(request):
    """
    View for 403 (Permission Denied) error.
    """
    return render(
        request, 'common/403.html', _get_context('Permission Denied'),
    )


def handler404(request, exception):
    """

    """
    return render(request, 'common/404.html', _get_context("Page Not Found"))


class ResetPassword(PasswordResetView):
    template_name = "password_reset/password_reset_form.html"


class ResetPasswordDone(PasswordResetDoneView):
    template_name = "password_reset/password_reset_done.html"


class ResetPasswordConfirm(PasswordResetConfirmView):
    template_name = "password_reset/password_reset_confirm.html"

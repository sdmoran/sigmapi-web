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

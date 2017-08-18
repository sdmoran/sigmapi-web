"""
Views for PubSite app.
"""
from django.shortcuts import render


def index(request):
    """
    View for the static index page
    """
    return render(request, 'public/home.html', None)


def history(request):
    """
    View for the static chapter history page.
    """
    return render(request, 'public/history.html', None)


def service(request):
    """
    View for the static chapter service page.
    """
    return render(request, 'public/service.html', None)


def donate(request):
    """
    View for the static donate page.
    """
    return render(request, 'public/donate.html', None)


def permission_denied(request):
    """
    View for 403 (Permission Denied) error.
    """
    return render(request, 'common/403.html', None)

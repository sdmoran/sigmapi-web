"""
Views for PubSite app.
"""
from django.shortcuts import render


_PAGES = {
    'Home': '/',
    'History': '/history',
    'Service': '/service',
    'Brothers':  '/brothers',
    'Log In': '/secure',
}


def index(request):
    """
    View for the static index page
    """
    return render(
        request, 'public/home2.html',
        {'pages': _PAGES, 'current_page_name': 'Home'},
    )


def history(request):
    """
    View for the static chapter history page.
    """
    return render(
        request, 'public/history.html',
        {'pages': _PAGES, 'current_page_name': 'History'},
    )


def service(request):
    """
    View for the static chapter service page.
    """
    return render(
        request, 'public/service.html',
        {'pages': _PAGES, 'current_page_name': 'Service'},
    )


def donate(request):
    """
    View for the static donate page.
    """
    return render(
        request, 'public/donate.html',
        {'pages': _PAGES, 'current_page_name': 'Donate'},
    )


def permission_denied(request):
    """
    View for 403 (Permission Denied) error.
    """
    return render(
        request, 'common/403.html',
        {'pages': _PAGES, 'current_page_name': 'Permission Denied'},
    )

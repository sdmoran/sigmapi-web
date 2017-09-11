"""
Views for Calendar app.
"""
from django.shortcuts import render


def manage_subscriptions(request):
    """
    TODO docstring
    """
    return render(request, 'calendar/manage_subscriptions.html')



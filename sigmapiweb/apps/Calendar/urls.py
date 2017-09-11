"""
URLs for Calendar app.
"""
from django.conf.urls import url
from django.views.generic import RedirectView

from . import api, views


urlpatterns = [
    url(
        regex=r'^$',
        view=RedirectView.as_view(
            pattern_name='calendar-manage_subscriptions',
            permanent=False,
        ),
    ),
    url(
        regex=r'^subscriptions/$',
        view=views.manage_subscriptions,
        name='calendar-manage_subscriptions',
    ),
    url(
        regex=r'^subscribe/(?P<calendar_name>[\w]+)$',
        view=views.subscribe,
        name='calendar-subscribe',
    ),
    url(
        regex=r'^unsubscribe/(?P<calendar_name>[\w]+)$',
        view=views.unsubscribe,
        name='calendar-unsubscribe',
    ),
]

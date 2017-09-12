"""
URLs for MailingList app.
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
        regex=r'^set_subscribed/(?P<calendar_name>[\w]+)$',
        view=views.set_subscribed,
        name='calendar-set_subscribed',
    ),
    url(
        regex=r'^sendinvite/$',
        view=api.send_invite,
        name='calendar-sendinvite',
    ),
]

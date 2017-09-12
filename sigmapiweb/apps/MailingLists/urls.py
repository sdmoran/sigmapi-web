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
            pattern_name='mailinglists-manage_subscriptions',
            permanent=False,
        ),
    ),
    url(
        regex=r'^subscriptions/$',
        view=views.manage_subscriptions,
        name='mailinglists-manage_subscriptions',
    ),
    url(
        regex=r'^set_subscribed/(?P<mailing_list_name>[\w]+)$',
        view=views.set_subscribed,
        name='mailinglists-set_subscribed',
    ),
    url(
        regex=r'^sendmail/$',
        view=api.send_mail,
        name='mailinglists-sendmail',
    ),
]

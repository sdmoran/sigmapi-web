"""
URLs for PubSite app.
"""
from django.conf.urls import url
from django.contrib.auth import views as dsl
from django.views.generic.base import RedirectView

from . import views
from . import models


urlpatterns = [
    url(
        regex=r'^login',
        view=dsl.login,
        name='pub-login',
    ),
    url(
        regex=r'^logout',
        view=dsl.logout_then_login,
        name='pub-logout',
    ),
    url(
        regex=r'^$',
        view=views.index,
        name='pub-index',
    ),
    url(
        regex=r'^history[/]$',
        view=RedirectView.as_view(pattern_name='pub-about'),
        name='pub-history',
    ),
    url(
        regex=r'^about[/]$',
        view=views.about,
        name='pub-about',
    ),
    url(
        regex=r'^service[/]$',
        view=RedirectView.as_view(pattern_name='pub-activities'),
        name='pub-service',
    ),
    url(
        regex=r'^activities[/]$',
        view=views.activities,
        name='pub-activities',
    ),
    url(
        regex=r'^403/',
        view=views.permission_denied,
        name='pub-permission_denied',
    ),
    url(
        regex=r'^donate/',
        view=views.donate,
        name='pub-donate',
    ),
]

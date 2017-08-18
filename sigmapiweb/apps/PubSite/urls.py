"""
URLs for PubSite app.
"""
from django.conf.urls import url
from django.contrib.auth import views as dsl

from . import views


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
        view=views.history,
        name='pub-history',
    ),
    url(
        regex=r'^service[/]$',
        view=views.service,
        name='pub-service',
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

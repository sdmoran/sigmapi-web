"""
URLs for PubSite app.
"""
from django.conf.urls import url
from django.contrib.auth import views as dsl
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views


from . import views


urlpatterns = [
    url(
        r'^password_reset/$',
        views.ResetPassword.as_view(),
        name='password_reset'
    ),
    url(
        r'^password_reset/done/$',
        views.ResetPasswordDone.as_view(),
        name='password_reset_done'
    ),
    url(
        r'^password_reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.ResetPasswordConfirm.as_view(),
        name='password_reset_confirm'
    ),
    url(
        r'^password_reset/complete/$',
        views.ResetPasswordComplete.as_view(),
        name='password_reset_complete'
    ),
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
]

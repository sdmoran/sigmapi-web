"""
URLs for public part of UserInfo app.
"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.users,
        name='userinfo-users',
    ),
    url(
        regex=r'^email/',
        view=views.change_email,
        name='userinfo-change_email',
    ),
    url(
        regex=r'^password/',
        view=views.change_password,
        name='userinfo-change_password',
    ),
]

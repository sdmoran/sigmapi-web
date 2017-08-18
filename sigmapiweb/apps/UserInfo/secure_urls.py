"""
URLs for secure part of UserInfo app.
"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.manage_users,
        name='userinfo-manage_users'
    ),
    url(
        regex=r'^add/',
        view=views.add_users,
        name='userinfo-add_users'
    ),
    url(
        regex=r'^edit/(?P<user>\w+)/$',
        view=views.edit_user,
        name='userinfo-edit_user'
    ),
    url(
        regex=r'^reset_password/(?P<user>\w+)/$',
        view=views.reset_password,
        name='userinfo-reset_password'
    ),
]

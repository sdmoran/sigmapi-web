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
        regex=r'^family-tree/$',
        view=views.family_tree_dashboard,
        name='userinfo-family_tree_dashbaord',
    ),
    url(
        regex=r'^family-tree/view/',
        view=views.family_tree,
        name='userinfo-family_tree'
    ),
    url(
        regex=r'^family-tree/data/',
        view=views.get_tree_json,
        name='userinfo-family_tree_data'
    ),
    url(
        regex=r'^password/',
        view=views.change_password,
        name='userinfo-change_password',
    ),
]

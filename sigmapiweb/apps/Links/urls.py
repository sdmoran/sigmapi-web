"""
URLs for Links app.
"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.view_all,
        name='links-view_all',
    ),
    url(
        regex=r'^add/$',
        view=views.add_link,
        name='links-add_link',
    ),
    url(
        regex=r'^(?P<link>[\d]+)/delete/$',
        view=views.delete_link,
        name='links-delete_link',
    ),
]

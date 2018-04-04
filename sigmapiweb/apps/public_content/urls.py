"""
URLs for Scholarship app.
"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.index,
        name='public-content-index',
    ),
    url(
        regex=r'^article$',
        view=views.article,
        name='public-content-article',
    ),
]

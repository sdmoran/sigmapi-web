from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    url(r'^$', views.index, name='archive-index'),

    # Bylaws
    url(r'^bylaws/$', views.bylaws, name='archive-bylaws'),
    url(r'^bylaws/(?P<bylaw>[\d]+)/$', views.download_bylaw, name='archive-download_bylaw'),
    url(r'^bylaws/delete/$', views.delete_bylaw, name='archive-delete_bylaw'),

    # House guides
    url(r'^guides/$', views.guides, name='archive-guides'),
    url(r'^guides/delete/$', views.delete_guide, name='archive-delete_guide'),
    url(r'^guides/(?P<guides>[\d]+)/$', views.download_guides, name='archive-download_guides'),

    # House rules
    url(r'^rules/$', views.rules, name='archive-rules'),
    url(r'^rules/delete/$', views.delete_rules, name='archive-delete_rules'),
    url(r'^rules/(?P<rules>[\d]+)/$', views.download_rules, name='archive-download_rules'),
]

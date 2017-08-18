"""
URLs for Archive app.
"""
from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^$',
        view=views.index,
        name='archive-index',
    ),

    # Bylaws
    url(
        regex=r'^bylaws/$',
        view=views.bylaws,
        name='archive-bylaws',
    ),
    url(
        regex=r'^bylaws/(?P<bylaw>[\d]+)/$',
        view=views.download_bylaw,
        name='archive-download_bylaw',
    ),
    url(
        regex=r'^bylaws/delete/$',
        view=views.delete_bylaw,
        name='archive-delete_bylaw',
    ),

    # House guides
    url(
        regex=r'^guides/$',
        view=views.guides,
        name='archive-guides',
    ),
    url(
        regex=r'^guides/delete/$',
        view=views.delete_guide,
        name='archive-delete_guide',
    ),
    url(
        regex=r'^guides/(?P<guides_id>[\d]+)/$',
        view=views.download_guides,
        name='archive-download_guides'
    ),

    # House rules
    url(
        regex=r'^rules/$',
        view=views.rules,
        name='archive-rules',
    ),
    url(
        regex=r'^rules/delete/$',
        view=views.delete_rules,
        name='archive-delete_rules',
    ),
    url(
        regex=r'^rules/(?P<rules_id>[\d]+)/$',
        view=views.download_rules,
        name='archive-download_rules',
    ),
]

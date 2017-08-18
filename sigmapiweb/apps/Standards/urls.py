"""
URLs for Standards app.
"""

from django.conf.urls import url
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    # Keep the old index URL for backwards compatibility.
    url(
        regex=r'^$',
        view=RedirectView.as_view(pattern_name='standards-index'),
        name='standards-index_old',
    ),
    url(
        regex=r'^overview/$',
        view=views.index,
        name='standards-index',
    ),
    url(
        regex=r'^summons/$',
        view=views.manage_summons,
        name='standards-manage_summons',
    ),
    url(
        regex=r'^summons/requests/$',
        view=views.manage_summons_requests,
        name='standards-manage_summons_requests',
    ),
    url(
        regex=r'^summons/approve/(?P<summons_req>[\d]+)/$',
        view=views.approve_summons_request,
        name='standards-approve_summons_request',
    ),
    url(
        regex=r'^summons/reject/(?P<summons_req>[\d]+)/$',
        view=views.reject_summons_request,
        name='standards-reject_summons_request',
    ),
    url(
        regex=r'^summons/request/$',
        view=views.send_summons_request,
        name='standards-send_summons_request',
    ),
    url(
        regex=r'^bones/summons/approve/(?P<summons>[\d]+)/$',
        view=views.accept_summons,
        name='standards-accept_summons',
    ),
    url(
        regex=r'^bones/summons/reject/(?P<summons>[\d]+)/$',
        view=views.delete_summons,
        name='standards-delete_summons',
    ),
]

from django.conf.urls import url
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='standards-index'), name='standards-index_old'), # Keep the old index URL for backwards compatibility.
    url(r'^overview/$', views.index, name='standards-index'),
    url(r'^summons/$', views.manage_summons, name='standards-manage_summons'),
    url(r'^summons/requests/$', views.manage_summons_requests, name='standards-manage_summons_requests'),
    url(r'^summons/approve/(?P<summons_req>[\d]+)/$', views.approve_summons_request, name='standards-approve_summons_request'),
    url(r'^summons/reject/(?P<summons_req>[\d]+)/$', views.reject_summons_request, name='standards-reject_summons_request'),
    url(r'^summons/request/$', views.send_summons_request, name='standards-send_summons_request'),
    url(r'^bones/summons/approve/(?P<summons>[\d]+)/$', views.accept_summons, name='standards-accept_summons'),
    url(r'^bones/summons/reject/(?P<summons>[\d]+)/$', views.delete_summons, name='standards-delete_summons'),
]

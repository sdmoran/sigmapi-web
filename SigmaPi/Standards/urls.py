from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='Standards.views.index')), # Keep the old index URL for backwards compatibility.
    url(r'^overview/$', 'Standards.views.index'),
    url(r'^summons/$', 'Standards.views.manage_summons'),
    url(r'^summons/requests/$', 'Standards.views.manage_summons_requests'),
    url(r'^summons/approve/(?P<summons_req>[\d]+)/$', 'Standards.views.approve_summons_request'),
    url(r'^summons/reject/(?P<summons_req>[\d]+)/$', 'Standards.views.reject_summons_request'),
    url(r'^summons/request/$', 'Standards.views.send_summons_request'),
    url(r'^bones/summons/approve/(?P<summons>[\d]+)/$', 'Standards.views.accept_summons'),
    url(r'^bones/summons/reject/(?P<summons>[\d]+)/$', 'Standards.views.delete_summons'),
)

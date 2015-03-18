from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('',
	url(r'^$', RedirectView.as_view(pattern_name='Standards.views.index')), # Keep the old index URL for backwards compatibility.
	url(r'^overview/$', 'Standards.views.index'),
	url(r'^summons/$', 'Standards.views.manage_summons'),
	url(r'^summons/new/$', 'Standards.views.create_new_summons'),
	url(r'^summons/approve/(?P<summons_req>[\d]+)/$', 'Standards.views.approve_summons_request'),
	url(r'^summons/reject/(?P<summons_req>[\d]+)/$', 'Standards.views.reject_summons_request'),
	url(r'^summons/request/$', 'Standards.views.send_summons_request'),
	url(r'^bones/$', 'Standards.views.edit_bones'),
	url(r'^bones/(?P<bone>[\d]+)/$', 'Standards.views.edit_bone'),
	url(r'^bones/(?P<bone>[\d]+)/expire/$', 'Standards.views.expire_bone'),
	url(r'^bones/(?P<bone>[\d]+)/reduce/$', 'Standards.views.reduce_bone'),
	url(r'^bones/add/', 'Standards.views.add_bone'),
	url(r'^bones/probation/add/', 'Standards.views.add_probation'),
	url(r'^bones/probation/(?P<probation>[\d]+)/delete', 'Standards.views.end_probation'),
	url(r'^bones/summons/approve/(?P<summons>[\d]+)/$', 'Standards.views.accept_summons'),
	url(r'^bones/summons/reject/(?P<summons>[\d]+)/$', 'Standards.views.reject_summons'),
	url(r'^points/$', 'Standards.views.manage_points'),
	url(r'^points/(?P<brother>[\d]+)/$', 'Standards.views.add_points'),
	url(r'^points/request/$', 'Standards.views.request_points'),
	url(r'^points/request/(?P<pointreq>[\d]+)/delete/$', 'Standards.views.delete_request'),
	url(r'^points/request/(?P<pointreq>[\d]+)/accept/$', 'Standards.views.accept_request'),
	url(r'^jobs/request/add/(?P<jobtype>[\d]+)/$', 'Standards.views.add_job_request'),
	url(r'^jobs/request/delete/(?P<jobrequest>[\d]+)/$', 'Standards.views.delete_job_request'),
	url(r'^jobs/request/take/(?P<jobrequest>[\d]+)/$', 'Standards.views.accept_job_request'),

)

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
	url(r'^$', 'Archive.views.index'),

	# Bylaws
	url(r'^bylaws/$', 'Archive.views.bylaws'),
	url(r'^bylaws/(?P<bylaw>[\d]+)/$', 'Archive.views.download_bylaw'),
	url(r'^bylaws/delete/$', 'Archive.views.delete_bylaw'),

	# House guides
	url(r'^guides/$', 'Archive.views.guides'),
	url(r'^guides/delete/$', 'Archive.views.delete_guide'),
	url(r'^guides/(?P<guides>[\d]+)/$', 'Archive.views.download_guides'),

	# House rules
	url(r'^rules/$', 'Archive.views.rules'),
	url(r'^rules/delete/$', 'Archive.views.delete_rules'),
	url(r'^rules/(?P<rules>[\d]+)/$', 'Archive.views.download_rules'),
)

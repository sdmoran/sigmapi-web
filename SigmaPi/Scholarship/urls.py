from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',

    # Viewing pages
	url(r'^$', 'Scholarship.views.index'),
	url(r'^study_hours/$', 'Scholarship.views.study_hours'),
	url(r'^resources/$', 'Scholarship.views.resources'),
	url(r'^library/$', 'Scholarship.views.library'),
	url(r'^approve/$', 'Scholarship.views.approve'),

	# Approve pages
	url(r'^approve/resource/(?P<resource>[\d]+)/$', 'Scholarship.views.approve_resource'),
	url(r'^approve/library/(?P<item>[\d]+)/$', 'Scholarship.views.approve_libraryitem'),

	url(r'^decline/resource/(?P<resource>[\d]+)/$', 'Scholarship.views.decline_resource'),
	url(r'^decline/library/(?P<item>[\d]+)/$', 'Scholarship.views.decline_libraryitem'),

	# Download pages
	url(r'^resources/(?P<resource>[\d]+)/$', 'Scholarship.views.download_resource'),
	url(r'^library/(?P<item>[\d]+)/$', 'Scholarship.views.download_libraryitem'),

	# Delete pages
	url(r'^library/(?P<item>[\d]+)/delete$', 'Scholarship.views.delete_libraryitem'),
	url(r'^resources/(?P<resource>[\d]+)/delete$', 'Scholarship.views.delete_resource'),

	# Actions to POST to
	url(r'^study_hours/update_requirements/$', 'Scholarship.views.update_requirements'),
	url(r'^study_hours/untrack/(?P<user>[\d]+)/$', 'Scholarship.views.untrack_user'),
	url(r'^study_hours/probation/(?P<user>[\d]+)/$', 'Scholarship.views.send_probation'),
	url(r'^study_hours/record_hours/$', 'Scholarship.views.record_hours'),
	url(r'^resources/upload/$', 'Scholarship.views.upload_resource'),
	url(r'^library/upload/$', 'Scholarship.views.upload_libraryitem'),
)


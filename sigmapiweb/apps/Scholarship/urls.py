from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [

    # Viewing pages
    url(r'^$', views.index, name='scholarship-index'),
    url(r'^study_hours/$', views.study_hours, name='scholarship-study_hours'),
    url(r'^resources/$', views.resources, name='scholarship-resources'),
    url(r'^library/$', views.library, name='scholarship-library'),
    url(r'^approve/$', views.approve, name='scholarship-approve'),

    # Approve pages
    url(r'^approve/resource/(?P<resource>[\d]+)/$', views.approve_resource, name='scholarship-approve_resource'),
    url(r'^approve/library/(?P<item>[\d]+)/$', views.approve_libraryitem, name='scholarship-approve_libraryitem'),

    url(r'^decline/resource/(?P<resource>[\d]+)/$', views.decline_resource, name='scholarship-decline_resource'),
    url(r'^decline/library/(?P<item>[\d]+)/$', views.decline_libraryitem, name='scholarship-decline_libraryitem'),

    # Download pages
    url(r'^resources/(?P<resource>[\d]+)/$', views.download_resource, name='scholarship-download_resource'),
    url(r'^library/(?P<item>[\d]+)/$', views.download_libraryitem, name='scholarship-download_libraryitem'),
    url(r'^study_hours/export$', views.download_hours, name='scholarship-export_hours'),

    # Delete pages
    url(r'^library/(?P<item>[\d]+)/delete$', views.delete_libraryitem, name='scholarship-delete_libraryitem'),
    url(r'^resources/(?P<resource>[\d]+)/delete$', views.delete_resource, name='scholarship-delete_resource'),

    # Actions to POST to
    url(r'^study_hours/update_requirements/$', views.update_requirements, name='scholarship-update_requirements'),
    url(r'^study_hours/untrack/(?P<user>[\d]+)/$', views.untrack_user, name='scholarship-untrack_user'),
    url(r'^study_hours/probation/(?P<user>[\d]+)/$', views.send_probation, name='scholarship-send_probation'),
    url(r'^study_hours/record_hours/$', views.record_hours, name='scholarship-record_hours'),
    url(r'^resources/upload/$', views.upload_resource, name='scholarship-upload_resource'),
    url(r'^library/upload/$', views.upload_libraryitem, name='scholarship-upload_libraryitem'),
]


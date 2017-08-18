"""
URLs for Scholarship app.
"""
from django.conf.urls import url

from . import views


urlpatterns = [

    # Viewing pages
    url(
        regex=r'^$',
        view=views.index,
        name='scholarship-index',
    ),
    url(
        regex=r'^study_hours/$',
        view=views.study_hours,
        name='scholarship-study_hours',
    ),
    url(
        regex=r'^resources/$',
        view=views.resources,
        name='scholarship-resources',
    ),
    url(
        regex=r'^library/$',
        view=views.library,
        name='scholarship-library',
    ),
    url(
        regex=r'^approve/$',
        view=views.approve,
        name='scholarship-approve',
    ),

    # Approve pages
    url(
        regex=r'^approve/resource/(?P<resource>[\d]+)/$',
        view=views.approve_resource,
        name='scholarship-approve_resource',
    ),
    url(
        regex=r'^approve/library/(?P<item>[\d]+)/$',
        view=views.approve_libraryitem,
        name='scholarship-approve_libraryitem',
    ),

    url(
        regex=r'^decline/resource/(?P<resource>[\d]+)/$',
        view=views.decline_resource,
        name='scholarship-decline_resource',
    ),
    url(
        regex=r'^decline/library/(?P<item>[\d]+)/$',
        view=views.decline_libraryitem,
        name='scholarship-decline_libraryitem',
    ),

    # Download pages
    url(
        regex=r'^resources/(?P<resource>[\d]+)/$',
        view=views.download_resource,
        name='scholarship-download_resource',
    ),
    url(
        regex=r'^library/(?P<item>[\d]+)/$',
        view=views.download_libraryitem,
        name='scholarship-download_libraryitem',
    ),
    url(
        regex=r'^study_hours/export$',
        view=views.download_hours,
        name='scholarship-export_hours',
    ),

    # Delete pages
    url(
        regex=r'^library/(?P<item>[\d]+)/delete$',
        view=views.delete_libraryitem,
        name='scholarship-delete_libraryitem',
    ),
    url(
        regex=r'^resources/(?P<resource>[\d]+)/delete$',
        view=views.delete_resource,
        name='scholarship-delete_resource',
    ),

    # Actions to POST to
    url(
        regex=r'^study_hours/update_requirements/$',
        view=views.update_requirements,
        name='scholarship-update_requirements',
    ),
    url(
        regex=r'^study_hours/untrack/(?P<user>[\d]+)/$',
        view=views.untrack_user,
        name='scholarship-untrack_user',
    ),
    url(
        regex=r'^study_hours/probation/(?P<user>[\d]+)/$',
        view=views.send_probation,
        name='scholarship-send_probation',
    ),
    url(
        regex=r'^study_hours/record_hours/$',
        view=views.record_hours,
        name='scholarship-record_hours',
    ),
    url(
        regex=r'^resources/upload/$',
        view=views.upload_resource,
        name='scholarship-upload_resource',
    ),
    url(
        regex=r'^library/upload/$',
        view=views.upload_libraryitem,
        name='scholarship-upload_libraryitem',
    ),
]

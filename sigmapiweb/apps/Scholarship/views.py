"""
Views for Scholarship app.
"""
import csv
import json
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.utils.datastructures import MultiValueDict
from django_downloadview import sendfile

from . import notify
from .models import (
    AcademicResource,
    LibraryItem,
    StudyHoursRecord,
    TrackedUser,
)
from .forms import (
    AcademicResourceForm,
    LibraryItemForm,
    StudyHoursRecordForm,
    TrackedUserForm,
)


def request_is_from_tracked_user(request):
    """
    Returns wehther the request is from a user who must log study hours.

    Returns: bool
    """
    return (
        TrackedUser.objects.filter(
            number_of_hours__gt=0,
            user=request.user
        ).count() == 1
    )


def request_is_from_scholarship_head(request):  # pylint: disable=invalid-name
    """
    Returns whether the request from the scholarship head user.

    Returns: bool
    """
    return request.user.has_perm('Scholarship.scholarship_head')


def get_currently_tracked_users():
    """
    Returns a queryset of TrackedUsers who must log study hours.

    Returns: Queryset
    """
    return TrackedUser.objects.filter(number_of_hours__gt=0)


@permission_required(
    'Scholarship.scholarship_head',
    login_url='pub-permission_denied',
)
def download_hours(_request):
    """
    Export hours from the db as a csv
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=study_hours.csv'
    records = StudyHoursRecord.objects.all()
    writer = csv.writer(response)
    writer.writerow([
        "Username",
        "Name",
        "# of Hours",
        "Reported Date",
        "Submission Timestamp",
    ])
    for record in records:
        writer.writerow([
            record.user.username,
            record.user.first_name + " " + record.user.last_name,
            record.number_of_hours,
            record.date,
            record.time_stamp,
        ])
    return response


@login_required
@require_GET
def index(_request):
    """
    TODO: Docstring
    """
    return redirect('scholarship-resources')


@login_required
@require_GET
def study_hours(request):
    """
    TODO: Docstring
    """
    # Figure out if this request is from the scholarship head
    is_scholarship_head = request_is_from_scholarship_head(request)

    # Figure out if this request is from a user who currently has their
    # study hours tracked
    is_tracked_user = request_is_from_tracked_user(request)

    # Initialize objects if necessary for the scholarship head
    currently_tracked_users = None
    update_requirements_form = None
    if is_scholarship_head:
        currently_tracked_users = get_currently_tracked_users()
        update_requirements_form = TrackedUserForm()

    # Initialize objects if necessary for a tracked user
    record_hours_form = None
    tracked_user_object = None
    tracked_user_records_this_week = None
    if is_tracked_user:
        record_hours_form = StudyHoursRecordForm()
        tracked_user_object = TrackedUser.objects.get(user=request.user)
        tracked_user_records = StudyHoursRecord.objects.filter(
            user=request.user
        ).order_by('-date')
        tracked_user_records_this_week = [
            record for record
            in tracked_user_records
            if record.happened_this_week()
        ]

    context = {
        'is_scholarship_head': is_scholarship_head,
        'is_tracked_user': is_tracked_user,
        'currently_tracked_users': currently_tracked_users,
        'update_requirements_form': update_requirements_form,
        'record_hours_form': record_hours_form,
        'tracked_user_object': tracked_user_object,
        'tracked_user_records_this_week': tracked_user_records_this_week
    }

    return render(request, 'scholarship/study_hours.html', context)


@permission_required(
    'Scholarship.scholarship_head',
    login_url='pub-permission_denied',
)
@require_POST
def update_requirements(request):
    """
    TODO: Docstring
    """
    update_requirements_form = TrackedUserForm(request.POST)
    if update_requirements_form.is_valid():
        tracked_user = update_requirements_form.save()

        if tracked_user.number_of_hours == 0:
            notify.study_hours_untracked(tracked_user)
        else:
            notify.study_hours_tracked(tracked_user)

        message = 'User\'s study hours requirement successfully updated.'
        messages.info(request, message, extra_tags='track')
    else:
        message = (
            'Both user name and number of hours ' +
            'is required. Number of hours cannot be < 0.',
        )
        messages.error(request, message, extra_tags='track')
    return redirect('scholarship-study_hours')


@permission_required(
    'Scholarship.scholarship_head',
    login_url='pub-permission_denied',
)
@require_POST
def untrack_user(request, user):
    """
    TODO: Docstring
    """
    tracked_user = TrackedUser.objects.get(pk=user)
    tracked_user.number_of_hours = 0
    tracked_user.save()
    notify.study_hours_untracked(tracked_user)
    message = 'User\'s study hours requirement successfully updated.'
    messages.info(request, message, extra_tags='track')
    return redirect('scholarship-study_hours')


@permission_required(
    'Scholarship.scholarship_head',
    login_url='pub-permission_denied',
)
@require_POST
def send_probation(request, user):
    """
    TODO: Docstring
    """
    tracked_user = TrackedUser.objects.get(pk=user)
    notify.social_probation(tracked_user)
    message = (
        'User has successfully been notified ' +
        'about their social probation.'
    )
    messages.info(request, message, extra_tags='track')
    return redirect('scholarship-study_hours')


@login_required
@require_POST
def record_hours(request):
    """
    TODO: Docstring
    """
    record_hours_form = StudyHoursRecordForm(request.POST)
    if record_hours_form.is_valid():
        study_hours_record = record_hours_form.save(commit=False)
        study_hours_record.user = request.user
        study_hours_record.save()

        message = 'Study hours successfully reported.'
        messages.info(request, message, extra_tags='report')
    else:
        message = (
            'You must input a positive number ' +
            'of hours studied. The date studied must ' +
            'have taken place this week and not ' +
            'in the future.'
        )
        messages.error(request, message, extra_tags='report')
    return redirect('scholarship-study_hours')


@login_required
@require_GET
def resources(request):
    """
    TODO: Docstring
    """
    is_scholarship_head = request_is_from_scholarship_head(request)
    upload_resource_form = None
    upload_resource_form = AcademicResourceForm()
    academic_resources = AcademicResource.objects.filter(approved=True)
    context = {
        'is_scholarship_head': is_scholarship_head,
        'upload_resource_form': upload_resource_form,
        'resources': academic_resources
    }
    return render(request, 'scholarship/resources.html', context)


@login_required
@require_POST
def upload_resource(request):
    """
    TODO: Docstring
    """

    # Retrieve the files from the MultiValueDictionary
    files = request.FILES.getlist("resource_pdf")
    # Iterate over the list of files, uploading them separately
    for file in files:
        # Build a MultiValueDictionary containing just this file
        # This is done simply because it is the required format of the
        # Academic Resource Form
        mvd = MultiValueDict()
        file_list = [file]
        mvd.setlist("resource_pdf", file_list)

        # Save the Files
        upload_resource_form = AcademicResourceForm(request.POST, mvd)
        # Check if the resource is valid
        if upload_resource_form.is_valid():
            # Save the resource
            resource = upload_resource_form.save(commit=False)
            # Get the resource name and extension
            file_name, extension = os.path.splitext(
                os.path.basename(resource.resource_pdf.name))
            # Set the resource name
            resource.resource_name = file_name
            if extension == ".pdf":
                if request_is_from_scholarship_head(request):
                    resource.approved = True
                    message = file_name + ' uploaded successfully!'
                else:
                    resource.approved = False
                    message = file_name + ' submitted for approval!'
                    notify.scholarship_content_submitted()

                resource.submittedBy = request.user
                resource.save()
                messages.info(request, message)
            else:
                messages.error(request, file_name + ' was not a pdf file.')
        else:
            message = (
                'Failed to upload resource. Make ' +
                'sure that you have provided all fields correctly.'
            )
            messages.error(request, message)

    # Can add additional response information here if needed in the future
    response = {}
    if request.META['HTTP_ACCEPT'] == 'application/json':
        content_type = 'application/json'
    else:
        content_type = 'text/plain'

    return HttpResponse(json.dumps(response), content_type=content_type)


@login_required
@require_GET
def download_resource(request, resource):
    """
    View for downloading a resource
    """
    resource_obj = AcademicResource.objects.get(pk=resource)
    allowed = (
        resource_obj.approved or
        request_is_from_scholarship_head(request)
    )
    if allowed:
        _, extension = os.path.splitext(
            os.path.basename(resource_obj.resource_pdf.name)
        )
        fname = resource_obj.resource_name + extension
        return sendfile(
            request,
            resource_obj.resource_pdf.path,
            attachment=True,
            attachment_filename=fname
        )
    return redirect('pub-permission_denied')


@permission_required(
    'Scholarship.scholarship_head',
    login_url='pub-permission_denied',
)
@require_POST
def delete_resource(_request, resource):
    """
    View for deleting a resource
    """

    resource_obj = AcademicResource.objects.get(pk=resource)
    resource_obj.resource_pdf.delete()  # Delete actual file

    resource_obj.delete()

    return redirect('scholarship-resources')


@login_required
@require_GET
def library(request):
    """
    TODO: Docstring
    """

    is_scholarship_head = request_is_from_scholarship_head(request)

    upload_item_form = None
    upload_item_form = LibraryItemForm()

    items = LibraryItem.objects.filter(approved=True)

    context = {
        'is_scholarship_head': is_scholarship_head,
        'upload_item_form': upload_item_form,
        'items': items
    }

    return render(request, 'scholarship/library.html', context)


@login_required
@require_POST
def upload_libraryitem(request):
    """
    TODO: Docstring
    """
    upload_item_form = LibraryItemForm(request.POST, request.FILES)

    if upload_item_form.is_valid():
        item = upload_item_form.save(commit=False)

        if request_is_from_scholarship_head(request):
            item.approved = True
            message = 'Item uploaded successfully!'
        else:
            item.approved = False
            message = 'Item submitted for approval successfully!'
            notify.scholarship_content_submitted()

        item.submittedBy = request.user

        item.save()

        messages.info(request, message)
    else:
        message = (
            'Failed to upload item. Make ' +
            'sure that you have provided all fields correctly.'
        )
        messages.error(request, message)

    # Can add additional response information here if needed in the future
    response = {}
    if request.META['HTTP_ACCEPT'] == 'application/json':
        content_type = 'application/json'
    else:
        content_type = 'text/plain'

    return HttpResponse(json.dumps(response), content_type=content_type)


@login_required
@require_GET
def download_libraryitem(request, item):
    """
    View for downloading a library item
    """
    item_obj = LibraryItem.objects.get(pk=item)
    allowed = item_obj.approved or request_is_from_scholarship_head(request)
    if allowed:
        _, extension = os.path.splitext(
            os.path.basename(item_obj.item_pdf.name)
        )
        fname = item_obj.title + extension

        return sendfile(
            request,
            item_obj.item_pdf.path,
            attachment=True,
            attachment_filename=fname
        )
    return redirect('pub-permission_denied')


@permission_required(
    'Scholarship.scholarship_head',
    login_url='pub-permission_denied',
)
@require_POST
def delete_libraryitem(_request, item):
    """
    View for deleting a library item
    """
    item_obj = LibraryItem.objects.get(pk=item)
    item_obj.item_pdf.delete()  # Delete actual file
    item_obj.delete()
    return redirect('scholarship-library')


@permission_required('Scholarship.scholarship_head',
                     login_url='pub-permission_denied')
@require_GET
def approve(request):
    """
    TODO: Docstring
    """
    pending_items = LibraryItem.objects.filter(approved=False)
    pending_resources = AcademicResource.objects.filter(approved=False)
    context = {
        'items': pending_items,
        'resources': pending_resources,
        'is_scholarship_head': request_is_from_scholarship_head(request)
    }
    return render(request, 'scholarship/approve.html', context)


@permission_required('Scholarship.scholarship_head',
                     login_url='pub-permission_denied')
@require_POST
def approve_resource(request, resource):
    """
    TODO: Docstring
    """
    try:
        resource_obj = AcademicResource.objects.get(pk=resource)
    except AcademicResource.DoesNotExist:
        messages.error(
            request,
            'The resource you tried to approve no longer exists.',
        )
    else:
        resource_obj.approved = True
        resource_obj.save()
        messages.info(
            request,
            'Resource approved successfully. It is now visible to all users.',
        )
    return redirect('scholarship-approve')


@permission_required(
    'Scholarship.scholarship_head',
    login_url='pub-permission_denied',
)
@require_POST
def decline_resource(request, resource):
    """
    TODO: Docstring
    """
    try:
        resource_obj = AcademicResource.objects.get(pk=resource)
    except AcademicResource.DoesNotExist:
        messages.error(
            request,
            'The resource you tried to decline has already been declined.',
        )
    else:
        resource_obj.resource_pdf.delete()  # Delete actual file
        resource_obj.delete()
        messages.info(request, 'Resource declined successfully.')
    return redirect('scholarship-approve')


@permission_required(
    'Scholarship.scholarship_head',
    login_url='pub-permission_denied',
)
@require_POST
def approve_libraryitem(request, item):
    """
    TODO: Docstring
    """
    try:
        item_obj = LibraryItem.objects.get(pk=item)
    except LibraryItem.DoesNotExist:
        messages.error(
            request,
            'The item you tried to approve no longer exists.',
        )
    else:
        item_obj.approved = True
        item_obj.save()
        messages.info(
            request,
            'Item approved successfully. It is now visible to all users.',
        )
    return redirect('scholarship-approve')


@permission_required(
    'Scholarship.scholarship_head',
    login_url='pub-permission_denied',
)
@require_POST
def decline_libraryitem(request, item):
    """
    TODO: Docstring
    """
    try:
        item_obj = LibraryItem.objects.get(pk=item)
    except LibraryItem.DoesNotExist:
        messages.error(
            request,
            'The Item you tried to decline has already been declined.',
        )
    else:
        item_obj.item_pdf.delete()  # Delete actual file
        item_obj.delete()
        messages.info(request, 'Item declined successfully.')
    return redirect('scholarship-approve')

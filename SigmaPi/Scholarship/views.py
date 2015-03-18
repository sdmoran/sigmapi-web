from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_GET, require_POST
from django.contrib import messages

from sendfile import sendfile

from Scholarship.models import TrackedUser, StudyHoursRecord, AcademicResource, LibraryItem
from Scholarship.forms import TrackedUserForm, StudyHoursRecordForm, AcademicResourceForm, LibraryItemForm
from Scholarship import notify

from django.http import HttpResponse
import json
import os

def request_is_from_tracked_user(request):
	"""
		Returns true if the request is from a user who is required to log more
		than 0 study hours per week.
	"""
	return TrackedUser.objects.filter(number_of_hours__gt=0, user=request.user).count() == 1


def request_is_from_scholarship_head(request):
	"""
		Returns true if the request from the scholarship head user.
	"""
	return request.user.has_perm('Scholarship.scholarship_head')


def get_currently_tracked_users():
	"""
		Returns a queryset of TrackedUser's who are required to record more than
		0 study hours per week.
	"""
	return TrackedUser.objects.filter(number_of_hours__gt=0)


@login_required
@require_GET
def index(request):
	return redirect('Scholarship.views.resources')


@login_required
@require_GET
def study_hours(request):

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
		tracked_user_records = StudyHoursRecord.objects.filter(user=request.user).order_by('-date')
		tracked_user_records_this_week = [record for record in tracked_user_records if record.happened_this_week()]

	context = {
		'is_scholarship_head': is_scholarship_head,
		'is_tracked_user': is_tracked_user,
		'currently_tracked_users': currently_tracked_users,
		'update_requirements_form': update_requirements_form,
		'record_hours_form': record_hours_form,
		'tracked_user_object': tracked_user_object,
		'tracked_user_records_this_week': tracked_user_records_this_week
	}

	return render(request, "scholarship_study_hours.html", context)

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def update_requirements(request):

	update_requirements_form = TrackedUserForm(request.POST)

	if update_requirements_form.is_valid():
		trackedUser = update_requirements_form.save()

		if trackedUser.number_of_hours == 0:
			notify.study_hours_untracked(trackedUser)
		else:
			notify.study_hours_tracked(trackedUser)


		messages.info(request, "User's study hours requirement successfully updated.", extra_tags="track")
	else:
		messages.error(request, "Both user name and number of hours is required. Number of hours cannot be < 0.", extra_tags="track")

	return redirect("Scholarship.views.study_hours")

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def untrack_user(request, user):

	trackedUser = TrackedUser.objects.get(pk=user)

	trackedUser.number_of_hours = 0
	trackedUser.save()

	notify.study_hours_untracked(trackedUser)
	messages.info(request, "User's study hours requirement successfully updated.", extra_tags="track")

	return redirect("Scholarship.views.study_hours")

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def send_probation(request, user):

	trackedUser = TrackedUser.objects.get(pk=user)

	notify.social_probation(trackedUser)
	messages.info(request, "User has successfully been notified about their social probation.", extra_tags="track")

	return redirect("Scholarship.views.study_hours")

@login_required
@require_POST
def record_hours(request):
	record_hours_form = StudyHoursRecordForm(request.POST)

	if record_hours_form.is_valid():
		study_hours_record = record_hours_form.save(commit=False)
		study_hours_record.user = request.user
		study_hours_record.save()

		messages.info(request, "Study hours successfully reported.", extra_tags="report")
	else:
		messages.error(request, "You must input a positive number of hours studied. The date studied must have taken place this week and not in the future.", extra_tags="report")

	return redirect("Scholarship.views.study_hours")


@login_required
@require_GET
def resources(request):

	is_scholarship_head = request_is_from_scholarship_head(request)

	upload_resource_form = None
	upload_resource_form = AcademicResourceForm()

	resources = AcademicResource.objects.filter(approved=True)

	context = {
		'is_scholarship_head': is_scholarship_head,
		'upload_resource_form': upload_resource_form,
		'resources': resources
	}

	return render(request, "scholarship_resources.html", context)

@login_required
@require_POST
def upload_resource(request):

	upload_resource_form = AcademicResourceForm(request.POST, request.FILES)

	if upload_resource_form.is_valid():
		resource = upload_resource_form.save(commit=False)

		if request_is_from_scholarship_head(request):
			resource.approved = True
			message = "Resource uploaded successfully!"
		else:
			resource.approved = False
			message = "Resource submitted for approval successfully!"
			notify.scholarship_content_submitted()

		resource.submittedBy = request.user

		resource.save()

		messages.info(request, message)
	else:
		messages.error(request, "Failed to upload resource. Make sure that you have provided all fields correctly.")

	# Can add additional response information here if needed in the future
	response = {}

	if request.META['HTTP_ACCEPT'] == 'application/json':
		contentType = "application/json"
	else:
		contentType = "text/plain"

	return HttpResponse(json.dumps(response), content_type=contentType)

@login_required
@require_GET
def download_resource(request, resource):
	"""
		View for downloading a resource
	"""

	resourceObject = AcademicResource.objects.get(pk=resource)

	allowed = resourceObject.approved or request_is_from_scholarship_head(request)

	if allowed:
		filepath, extension = os.path.splitext(os.path.basename(resourceObject.resource_pdf.name))
		fileName = resourceObject.resource_name + extension

		return sendfile(request, resourceObject.resource_pdf.path, attachment=True, attachment_filename=fileName)
	else:
		return redirect("PubSite.views.permission_denied")

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def delete_resource(request, resource):
	"""
		View for deleting a resource
	"""

	resourceObject = AcademicResource.objects.get(pk=resource)
	resourceObject.resource_pdf.delete() # Delete actual file

	resourceObject.delete()


	return redirect("Scholarship.views.resources")

@login_required
@require_GET
def library(request):

	is_scholarship_head = request_is_from_scholarship_head(request)

	upload_item_form = None
	upload_item_form = LibraryItemForm()

	items = LibraryItem.objects.filter(approved=True)

	context = {
		'is_scholarship_head': is_scholarship_head,
		'upload_item_form': upload_item_form,
		'items': items
	}

	return render(request, "scholarship_library.html", context)

@login_required
@require_POST
def upload_libraryitem(request):

	upload_item_form = LibraryItemForm(request.POST, request.FILES)

	if upload_item_form.is_valid():
		item = upload_item_form.save(commit=False)

		if request_is_from_scholarship_head(request):
			item.approved = True
			message = "Item uploaded successfully!"
		else:
			item.approved = False
			message = "Item submitted for approval successfully!"
			notify.scholarship_content_submitted()

		item.submittedBy = request.user

		item.save()

		messages.info(request, message)
	else:
		messages.error(request, "Failed to upload item. Make sure that you have provided all fields correctly.")

	# Can add additional response information here if needed in the future
	response = {}

	if request.META['HTTP_ACCEPT'] == 'application/json':
		contentType = "application/json"
	else:
		contentType = "text/plain"

	return HttpResponse(json.dumps(response), content_type=contentType)

@login_required
@require_GET
def download_libraryitem(request, item):
	"""
		View for downloading a library item
	"""

	itemObject = LibraryItem.objects.get(pk=item)

	allowed = itemObject.approved or request_is_from_scholarship_head(request)

	if allowed:
		filepath, extension = os.path.splitext(os.path.basename(itemObject.item_pdf.name))
		fileName = itemObject.title + extension

		return sendfile(request, itemObject.item_pdf.path, attachment=True, attachment_filename=fileName)
	else:
		return redirect("PubSite.views.permission_denied")

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def delete_libraryitem(request, item):
	"""
		View for deleting a library item
	"""

	itemObject = LibraryItem.objects.get(pk=item)

	itemObject.item_pdf.delete() # Delete actual file
	itemObject.delete()

	return redirect("Scholarship.views.library")

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_GET
def approve(request):
	pendingItems = LibraryItem.objects.filter(approved=False)
	pendingResources = AcademicResource.objects.filter(approved=False)

	context = {
		'items': pendingItems,
		'resources': pendingResources,
		'is_scholarship_head': request_is_from_scholarship_head(request)
	}

	return render(request, "scholarship_approve.html", context)

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def approve_resource(request, resource):
	try:
		resourceObject = AcademicResource.objects.get(pk=resource)

		resourceObject.approved = True
		resourceObject.save()

		messages.info(request, "Resource approved successfully. It is now visible to all users.")
	except:
		messages.error(request, "The resource you tried to approve no longer exists.")

	return redirect("Scholarship.views.approve")

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def approve_libraryitem(request, item):
	try:
		itemObject = LibraryItem.objects.get(pk=item)

		itemObject.approved = True
		itemObject.save()

		messages.info(request, "Item approved successfully. It is now visible to all users.")
	except:
		messages.error(request, "The item you tried to approve no longer exists.")

	return redirect("Scholarship.views.approve")

@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def decline_libraryitem(request, item):
	try:
		itemObject = LibraryItem.objects.get(pk=item)

		itemObject.item_pdf.delete() # Delete actual file
		itemObject.delete()

		messages.info(request, "Item declined successfully.")
	except:
		messages.error(request, "The Item you tried to decline has already been declined.")

	return redirect("Scholarship.views.approve")


@permission_required('Scholarship.scholarship_head', login_url='PubSite.views.permission_denied')
@require_POST
def decline_resource(request, resource):
	try:
		resourceObject = AcademicResource.objects.get(pk=resource)
		resourceObject.resource_pdf.delete() # Delete actual file

		resourceObject.delete()

		messages.info(request, "Resource declined successfully.")
	except:
		messages.error(request, "The resource you tried to decline has already been declined.")

	return redirect("Scholarship.views.approve")


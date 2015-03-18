from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.utils.html import strip_tags
from django.utils import dateformat

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.models import User

from datetime import datetime
from django.core.mail import send_mail

from Standards.models import JobRequest, Bone, PiPointsRecord, PiPointsRequest, PiPointsChangeRecord, Probation, BoneChangeRecord, SummonsRequest, Summons, SummonsHistoryRecord
from Standards.forms import JobRequestForm, PiPointsRequestForm, PiPointsAddBrotherForm, ProbationGivingForm, BoneGivingForm, BoneEditingForm, SummonsRequestForm, AddSummonsForm, AcceptSummonsForm
from Standards import notify

import json

@login_required
def index(request):
	"""
		Displays the homepage of the standards module.
	"""

	current_bones = Bone.objects.filter(bonee=request.user, expirationDate__gt=datetime.now()).order_by('-expirationDate')
	expired_bones = Bone.objects.filter(bonee=request.user, expirationDate__lte=datetime.now()).order_by('-expirationDate')
	current_bone_count = current_bones.count()

	point_records = PiPointsRecord.objects.all().exclude(brother__groups__name='Alumni').order_by('-points')

	own_points = PiPointsRecord.objects.filter(brother=request.user)

	if own_points.count() == 0:
		# If we don't have a record, create one.
		record = PiPointsRecord()
		record.points = 0
		record.jobsTaken = 0
		record.brother = request.user
		record.save()
		own_points = record
	else:
		own_points = own_points[0]

	probation = Probation.objects.filter(recipient=request.user, expirationDate__gt=datetime.now()).exists()
	points_form = PiPointsRequestForm()
	job_givers = JobRequest.objects.filter(takingJob=False).exclude(requester=request.user)
	job_doers = JobRequest.objects.filter(takingJob=True).exclude(requester=request.user)
	own_givers = JobRequest.objects.filter(takingJob=False, requester=request.user)
	own_doers = JobRequest.objects.filter(takingJob=True, requester=request.user)
	jobs_form = JobRequestForm()

	summons_form = SummonsRequestForm()

	requests_count = JobRequest.objects.all().count()
	pprCount = PiPointsRequest.objects.all().count()
	positive_points = own_points.points > 0

	error = None
	msg = None

	try:
		error = request.session['standards_index_error']
		del request.session['standards_index_error']
	except KeyError:
		pass

	try:
		msg = request.session['standards_index_msg']
		del request.session['standards_index_msg']
	except KeyError:
		pass


	context = {
	'current_bone_count': current_bone_count,
	'current_bones': current_bones,
	'expired_bones': expired_bones,
	'own_points': own_points,
	'point_records': point_records,
	'probation': probation,
	'points_form': points_form,
	'job_givers':job_givers,
	'job_doers':job_doers,
	'own_doers': own_doers,
	'own_givers': own_givers,
	'jobs_form': jobs_form,
	'positive_points': positive_points,
	'error': error,
	'requests_count': requests_count,
	'pprCount': pprCount,
	'summons_form': summons_form,
	'msg': msg,
	}

	return render(request, "secure/standards_index.html", context)

@permission_required('Standards.add_pipointsrequest', login_url='PubSite.views.permission_denied')
def request_points(request):
	"""
		Registers a pi point request to be reviewed by the friendly neighborhood parliamentarian
	"""
	if request.method == 'POST':
		form = PiPointsRequestForm(request.POST)

		if form.is_valid():
			ppr = form.save(commit=False)
			ppr.requester = request.user
			ppr.date = datetime.now()
			ppr.save()
			notify.points_requested() # Email notification to standards board
			request.session['standards_index_msg'] = "Pi Points request successfully submitted!"

		return redirect(index)
	else:
		return redirect(index)

@permission_required('Standards.add_bone', login_url='PubSite.views.permission_denied')
def edit_bones(request):
	"""
		View for editing/managing all bones and punishments
	"""

	all_bones = Bone.objects.filter(expirationDate__gt=datetime.now()).order_by('-dateReceived')
	expired_bones = Bone.objects.filter(expirationDate__lte=datetime.now())
	all_probations = Probation.objects.filter(expirationDate__gt=datetime.now()).order_by('-dateReceived')

	all_summons = Summons.objects.order_by('-dateSummonsSent')

	summons_history = SummonsHistoryRecord.objects.all().order_by('-date')

	bone_edit_history = BoneChangeRecord.objects.all().order_by('-dateChangeMade')
	probation_form = ProbationGivingForm()
	bone_form = BoneGivingForm()
	pprCount = PiPointsRequest.objects.all().count()

	accept_summons_form = AcceptSummonsForm()

	error = None
	msg = None

	try:
		error = request.session['standards_bone_error']
		del request.session['standards_bone_error']
	except KeyError:
		pass

	try:
		msg = request.session['standards_bone_msg']
		del request.session['standards_bone_msg']
	except KeyError:
		pass

	context = {
	'active_bones': all_bones,
	'expired_bones': expired_bones,
	'all_probations': all_probations,
	'all_summons': all_summons,
	'probation_form': probation_form,
	'bone_form': bone_form,
	'bone_edit_history': bone_edit_history,
	'pprCount': pprCount,
	'error': error,
	'msg': msg,
	'accept_summons_form': accept_summons_form,
	'summons_history': summons_history
	}

	return render(request, "secure/standards_bones.html", context)

@permission_required('Standards.change_bone', login_url='PubSite.views.permission_denied')
def edit_bone(request, bone):
	"""
		View for editing a single bone.
	"""

	try:
		targetBone = Bone.objects.get(pk=bone)
		expired = targetBone.expirationDate <= datetime.now().date()
	except:
		return redirect('PubSite.views.permission_denied')

	if request.method == 'POST':
		if expired:
			return redirect('PubSite.views.permission_denied')

		oldReason = targetBone.reason
		oldPerson = targetBone.bonee
		oldExpiration = targetBone.expirationDate
		form = BoneEditingForm(request.POST, instance=targetBone)

		if form.is_valid():
			bone = form.save()
			if not bone.bonee == oldPerson:
				bone.bonee = oldPerson
				bone.save()
			record = BoneChangeRecord()
			record.bone = targetBone
			record.modifier = request.user
			record.dateChangeMade = datetime.now()
			record.previousReason = oldReason
			record.newReason = targetBone.reason
			record.previousExpirationDate = oldExpiration
			record.newExpirationDate = targetBone.expirationDate
			record.save()

			notify.bone_changed(bone) # Email notification to user/EC

		return redirect('Standards.views.edit_bones')
	else:
		bone_history = BoneChangeRecord.objects.filter(bone=targetBone).order_by('-dateChangeMade')

		if not expired:
			bone_form = BoneEditingForm(instance=targetBone)
		else:
			bone_form = None
		pprCount = PiPointsRequest.objects.all().count()
		context = {
			'bone': targetBone,
			'expired': expired,
			'bone_form': bone_form,
			'bone_history': bone_history,
			'pprCount': pprCount
			}

		return render(request, "secure/standards_edit_bone.html", context)

@permission_required('Standards.delete_bone', login_url='PubSite.views.permission_denied')
def expire_bone(request, bone):
	"""
		View for expiring a single bone.
	"""

	try:
		targetBone = Bone.objects.get(pk=bone)
		expired = targetBone.expirationDate <= datetime.now().date()
	except:
		return redirect('Standards.views.edit_bones')

	if request.method == 'POST':
		if expired:
			return redirect('Standards.views.edit_bones')

		oldExpirationDate = targetBone.expirationDate
		targetBone.expirationDate = datetime.now()
		targetBone.save()

		record = BoneChangeRecord()
		record.bone = targetBone
		record.modifier = request.user
		record.dateChangeMade = datetime.now()
		record.previousReason = targetBone.reason
		record.newReason = targetBone.reason
		record.previousExpirationDate = oldExpirationDate
		record.newExpirationDate = targetBone.expirationDate
		record.save()

		notify.bone_changed(targetBone) # Email notification to user/EC

		request.session['standards_bone_msg'] = "Bone successfully expired!"
		return redirect(edit_bones)
	else:
		return redirect('Standards.views.edit_bones')

@permission_required('Standards.add_bone', login_url='PubSite.views.permission_denied')
def add_bone(request):
	"""
		View for adding a new bone.
	"""
	if request.method == 'POST':
		form = BoneGivingForm(request.POST)

		if form.is_valid():
			bone = form.save(commit=False)
			bone.boner = request.user
			bone.dateReceived = datetime.now()
			bone.save()

			record = BoneChangeRecord()
			record.bone = bone
			record.modifier = request.user
			record.dateChangeMade = datetime.now()
			record.previousReason = "CREATED"
			record.newReason = bone.reason
			record.previousExpirationDate = bone.expirationDate
			record.newExpirationDate = bone.expirationDate
			record.save()

			notify.bone_received(bone)

			request.session['standards_bone_msg'] = "Bone successfully added!"
		return redirect(edit_bones)
	else:
		return redirect('Standards.views.edit_bones')

@login_required
def reduce_bone(request, bone):
	"""
		View for reducing a bone.
	"""
	if request.method == 'POST':
		targetBone = Bone.objects.get(pk=bone)

		if not targetBone.bonee == request.user:
			return redirect('PubSite.views.permission_denied')
		else:
			pointsRecord = PiPointsRecord.objects.get(brother=request.user)

			if pointsRecord.points <= 0 or pointsRecord.jobsTaken <= 0:
				request.session['standards_index_error'] = "You cannot reduce a bone! You don't have enough Pi Points or jobs taken."
				return redirect(index)
			elif pointsRecord.points < targetBone.value:
				targetBone.value = targetBone.value - pointsRecord.points
				targetBone.save()
				pointsRecord.points = 0
				pointsRecord.jobsTaken = pointsRecord.jobsTaken - 1
				pointsRecord.save()
			else:
				pointsRecord.points = pointsRecord.points - targetBone.value
				pointsRecord.jobsTaken = pointsRecord.jobsTaken - 1
				pointsRecord.save()
				targetBone.expirationDate = datetime.now()
				targetBone.save()

			request.session['standards_index_msg'] = "Bone successfully reduced!"
			return redirect(index)
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Standards.add_probation', login_url='PubSite.views.permission_denied')
def add_probation(request):
	"""
		View for adding a new probation.
	"""
	if request.method == 'POST':
		form = ProbationGivingForm(request.POST)

		if form.is_valid():
			probation = form.save(commit=False)
			probation.giver = request.user
			probation.dateReceived = datetime.now()
			probation.save()
			notify.probation_received(probation)

		request.session['standards_bone_msg'] = "Probation successfully added!"

		return redirect(edit_bones)
	else:
		return redirect('Standards.views.edit_bones')

@permission_required('Standards.delete_probation', login_url='PubSite.views.permission_denied')
def end_probation(request, probation):
	"""
		View for ending a social probation.
	"""
	if request.method == 'POST':
		probation = Probation.objects.get(pk=probation)
		probation.expirationDate = datetime.now()
		probation.save()

		request.session['standards_bone_msg'] = "Probation successfully ended!"
		return redirect(edit_bones)
	else:
		return redirect('Standards.views.edit_bones')


@permission_required('Standards.add_pipointsrecord', login_url='PubSite.views.permission_denied')
def manage_points(request):
	"""
		Provides a view for managing pi points
	"""

	point_records = PiPointsRecord.objects.all().exclude(brother__groups__name='Alumni').order_by('-points')
	point_requests = PiPointsRequest.objects.all()
	point_changes = PiPointsChangeRecord.objects.all().order_by('-dateChanged')
	add_brother_form = PiPointsAddBrotherForm()
	pprCount = PiPointsRequest.objects.all().count()

	context = {
	'point_records': point_records,
	'point_requests': point_requests,
	'add_brother_form': add_brother_form,
	'point_changes': point_changes,
	'pprCount': pprCount,
	}

	return render(request, "secure/standards_points.html", context)

@permission_required('Standards.add_pipointsrecord', login_url='PubSite.views.permission_denied')
def add_points(request, brother):
	"""
		View for adding points to a given brother.
	"""
	if request.method == 'POST':
		try:
			points = int(strip_tags(request.POST['piPoints']))
			changeRecord = PiPointsChangeRecord()
			record = PiPointsRecord.objects.filter(pk=brother)
			if record.exists():
				targetRecord = record[0]
				old_points = targetRecord.points
				targetRecord.points = points
				targetRecord.save()

				changeRecord.oldValue = old_points
			else:
				user = User.objects.get(pk=brother)
				targetRecord = PiPointsRecord(brother=user)
				targetRecord.points = points
				targetRecord.save()
				changeRecord.oldValue = 0
		except:
			return redirect('PubSite.views.permission_denied')

		changeRecord.brother = targetRecord
		changeRecord.modifier = request.user
		changeRecord.dateChanged = datetime.now()
		changeRecord.newValue = targetRecord.points
		changeRecord.save()

		notify.points_changed(changeRecord)

		response = {}
		response['id'] = targetRecord.pk
		response['name'] = targetRecord.brother.first_name + ' ' + targetRecord.brother.last_name
		response['old_points'] = changeRecord.oldValue
		response['points'] = targetRecord.points
		response['date'] = dateformat.format(changeRecord.dateChanged, 'F j, Y, P')
		response['modifier'] = changeRecord.modifier.first_name + ' ' + changeRecord.modifier.last_name

		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Standards.delete_pipointsrequest', login_url='PubSite.views.permission_denied')
def accept_request(request, pointreq):
	"""
		View for accepting points request
	"""

	if request.method == 'POST':
		ppr = PiPointsRequest.objects.get(pk=pointreq)
		pointsAwarded = ppr.pointsForReason(ppr.reason)
		record = PiPointsRecord.objects.filter(pk=ppr.requester)
		changeRecord = PiPointsChangeRecord()

		targetRecord = record[0]
		changeRecord.oldValue = targetRecord.points
		targetRecord.points = targetRecord.points + pointsAwarded
		targetRecord.save()

		changeRecord.brother = targetRecord
		changeRecord.modifier = request.user
		changeRecord.dateChanged = datetime.now()
		changeRecord.newValue = targetRecord.points
		changeRecord.save()

		notify.points_changed(changeRecord)

		ppr.delete()

		response = {}
		response['id'] = targetRecord.pk
		response['name'] = targetRecord.brother.first_name + ' ' + targetRecord.brother.last_name
		response['old_points'] = changeRecord.oldValue
		response['points'] = targetRecord.points
		response['date'] = dateformat.format(changeRecord.dateChanged, 'F j, Y, P')
		response['modifier'] = changeRecord.modifier.first_name + ' ' + changeRecord.modifier.last_name
		response['pprCount'] = PiPointsRequest.objects.all().count()
		return HttpResponse(json.dumps(response), content_type="application/json")
	else:
		return redirect('PubSite.views.permission_denied')

@permission_required('Standards.delete_pipointsrequest', login_url='PubSite.views.permission_denied')
def delete_request(request, pointreq):
	"""
		View for denying points request
	"""

	if request.method == 'POST':
		request = PiPointsRequest.objects.get(pk=pointreq)

		notify.point_request_denied(request)

		request.delete()

	response = {}
	response['pprCount'] = PiPointsRequest.objects.all().count()
	return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def add_job_request(request, jobtype):

	if request.method == 'POST':
		form = JobRequestForm(request.POST)
		takingJob = jobtype == '2'

		pipoints = PiPointsRecord.objects.get(brother=request.user)

		if form.is_valid():
			jobreq = form.save(commit=False)

			# If looking for cover, make sure we have enough pi points
			if not takingJob:
				cost = jobreq.REASON_POINTS[jobreq.job]
				if cost > pipoints.points:
					request.session['standards_index_error'] = 'Could not submit job request, you do not have enough Pi Points!'
					return redirect(index)
				else:
					# Check all outstanding requests
					all_req = JobRequest.objects.filter(requester=request.user, takingJob=False)
					runningTally = cost
					for req in all_req:
						runningTally = runningTally + req.REASON_POINTS[req.job]
						if runningTally > pipoints.points:
							request.session['standards_index_error'] = 'Could not submit job request.  You do not have enough Pi Points to satisfy all your outstanding requests.'
							return redirect(index)
			jobreq.requester = request.user
			jobreq.takingJob = takingJob
			jobreq.date = datetime.now()
			jobreq.save()

			notify.job_requested(jobreq)

			request.session['standards_index_msg'] = "Job request successfully added!"
			return redirect(index)
		else:
			request.session['standards_index_error'] = form.errors
			return redirect(index)
	else:
		return redirect(index)

@login_required
def delete_job_request(request, jobrequest):
	if request.method == 'POST':
		try:
			jobreq = JobRequest.objects.get(pk=jobrequest)
		except:
			request.session['standards_index_error'] = "Sorry, that request cannot be deleted.  Somebody has already accepted the request."
			return redirect(index)

		if jobreq.requester == request.user:
			jobreq.delete()

			request.session['standards_index_msg'] = "Job request successfully deleted!"
			return redirect(index)
		else:
			return redirect('PubSite.views.permission_denied')
	else:
		return redirect(index)

@login_required
def accept_job_request(request, jobrequest):
	"""
		When a job request is accepted:
			A Pi Point request is sent for the user who is covering the job.
			The user whose job is being covered is docked pi points
			the request is deleted
	"""

	if request.method == 'POST':
		try:
			jobreq = JobRequest.objects.get(pk=jobrequest)
		except:
			request.session['standards_index_error'] = "Sorry, that request no longer exists.  Either the person who put it up deleted it or somebody else already accepted it."
			return redirect(index)

		# If its a job request where the requester is taking the job, they'll get the pi points
		if jobreq.takingJob:

			# Check that the giver has enough points
			takingBrother = jobreq.requester
			giverRecord = PiPointsRecord.objects.get(brother=request.user)
			currentRecord = giverRecord
			if giverRecord.points < jobreq.REASON_POINTS[jobreq.job]:
				request.session['standards_index_error'] = "You do not have enough Pi Points to have someone cover this job."
				return redirect(index)

		else:
			takingBrother = request.user
			giverRecord = PiPointsRecord.objects.get(brother=jobreq.requester)
			currentRecord = PiPointsRecord.objects.get(brother=request.user)

		# Send a request for the taker
		ppr = PiPointsRequest()
		ppr.requester = takingBrother
		ppr.reason = jobreq.job
		ppr.witness = "Took a job through Pi Point Web System."
		ppr.date = datetime.now()
		ppr.save()

		# Subtract pi points from giver
		giverRecord.points = giverRecord.points - jobreq.REASON_POINTS[jobreq.job]
		giverRecord.save()

		takerRecord = PiPointsRecord.objects.get(brother=takingBrother)
		takerRecord.jobsTaken = takerRecord.jobsTaken + 1
		takerRecord.save()

		notify.alertAboutJob(giverRecord, takingBrother, jobreq.get_job_display(), jobreq.details)

		jobreq.delete()
		request.session['standards_index_msg'] = "Job successfully taken!"
		return redirect(index)
	else:
		return redirect(index)

@permission_required('Standards.add_summonsrequest', login_url='PubSite.views.permission_denied')
def send_summons_request(request):
	"""
		A view for sending a summons request.
	"""

	if request.method == 'POST':

		numRecipients = int(request.POST["recipient-count"])

		# Check for reason
		reason = request.POST["reason"]
		if len(reason.strip()) == 0:
			request.session['standards_index_error'] = "Summons request failed to send. You must include a reason with the request."
			return redirect(index)

		# Check for recipients
		summonsSent = 0
		for i in range(numRecipients):
			try:
				if i == 0:
					currentRecipient = request.POST["summonee"]
				else:
					currentRecipient = request.POST["summonee_" + str(i + 1)]

				if len(currentRecipient.strip()) > 0:
					recipientInt = int(currentRecipient)

					recipientUser = User.objects.get(pk=recipientInt)

					summonsReq = SummonsRequest(summoner=request.user, summonee=recipientUser, reason=reason, dateRequestSent=datetime.now())
					summonsReq.save()

					summonsSent = summonsSent + 1
			except:
				request.session['standards_index_error'] = "Unknown error occurred while processing summons recipient list. Please try again. If the problem persists, please contact the Web Chair."
				return redirect(index)

		if summonsSent > 0:
			request.session['standards_index_msg'] = "Summons request sent successfully!"

			notify.summons_requested(summonsSent)

			return redirect(index)
		else:
			request.session['standards_index_error'] = "Summons request failed to send. You must include atleast 1 recipient with the request."
			return redirect(index)


	return redirect(index)

@permission_required('Standards.delete_summonsrequest', login_url='PubSite.views.permission_denied')
def manage_summons(request):
	"""
		A view for managing summons requests and sending out summons.
	"""

	current_requests = SummonsRequest.objects.all().order_by('-dateRequestSent')

	add_summon_form = AddSummonsForm()

	pprCount = PiPointsRequest.objects.all().count()

	error = None
	msg = None

	try:
		error = request.session['standards_summons_error']
		del request.session['standards_summons_error']
	except KeyError:
		pass

	try:
		msg = request.session['standards_summons_msg']
		del request.session['standards_summons_msg']
	except KeyError:
		pass

	context = {
		'current_requests': current_requests,
		'add_summon_form': add_summon_form,
		'error': error,
		'msg': msg,
		'pprCount': pprCount
		}

	return render(request, "secure/standards_summons.html", context)

@permission_required('Standards.delete_summonsrequest', login_url='PubSite.views.permission_denied')
def reject_summons_request(request, summons_req):
	"""
		A view for denying a summons request.
	"""

	if request.method == 'POST':
		try:
			summons_request = SummonsRequest.objects.get(pk=summons_req)
		except:
			request.session['standards_summons_error'] = "Sorry, that summons request no longer exists. It may have been approved or rejected already."
			return redirect(manage_summons)

		notify.summons_request_denied(summons_request)

		summons_request.delete()
		request.session['standards_summons_msg'] = "Summons request successfully rejected."
		return redirect(manage_summons)
	else:
		return redirect(manage_summons)


@permission_required('Standards.add_summons', login_url='PubSite.views.permission_denied')
def approve_summons_request(request, summons_req):
	"""
		A view for approving a summons request.
	"""
	if request.method == 'POST':
		try:
			summons_request = SummonsRequest.objects.get(pk=summons_req)
		except:
			request.session['standards_summons_error'] = "Sorry, that summons request no longer exists. It may have been approved or rejected already."
			return redirect(manage_summons)

		approved_summons = Summons()
		approved_summons.summoner = summons_request.summoner
		approved_summons.summonee = summons_request.summonee
		approved_summons.approver = request.user
		approved_summons.reason = summons_request.reason
		approved_summons.dateSummonsSent = datetime.now()

		approved_summons.save()
		summons_request.delete()

		notify.summons_sent(approved_summons)

		request.session['standards_summons_msg'] = "Summons request successfully accepted."
		return redirect(manage_summons)
	else:
		return redirect(manage_summons)

@permission_required('Standards.add_summons', login_url='PubSite.views.permission_denied')
def create_new_summons(request):
	"""
		A view for creating a new summons.
	"""
	if request.method == 'POST':
		form = AddSummonsForm(request.POST)

		if form.is_valid():
			summons = form.save(commit=False)

			summons.dateSummonsSent = datetime.now()
			summons.approver = request.user
			summons.save()

			notify.summons_sent(summons)

			request.session['standards_summons_msg'] = "Summons sent successfully."
		else:
			request.session['standards_summons_error'] = "Summons failed to be sent: " + str(form.errors)

		return redirect(manage_summons)
	else:
		return redirect(manage_summons)

@permission_required('Standards.add_summons', login_url='PubSite.views.permission_denied')
def accept_summons(request, summons):
	"""
		Accept a summons and turn it into a bone.
	"""

	if request.method == 'POST':
		try:
			summons_obj = Summons.objects.get(pk=summons)
		except:
			request.session['standards_bone_error'] = "Sorry, that summons no longer exists. It may have been approved or rejected already."
			return redirect(edit_bones)

		form = AcceptSummonsForm(request.POST)

		if form.is_valid():
			bone = form.save(commit=False)

			bone.dateReceived = summons_obj.dateSummonsSent
			bone.boner = request.user
			bone.bonee = summons_obj.summonee

			bone.save()

			summonsHistory = SummonsHistoryRecord()
			summonsHistory.summonee = summons_obj.summonee
			summonsHistory.summoner = summons_obj.summoner
			summonsHistory.details = summons_obj.reason
			summonsHistory.resultReason = bone.reason
			summonsHistory.date = datetime.now()
			summonsHistory.boneID = bone.id
			summonsHistory.hasBone = True
			summonsHistory.save()

			summons_obj.delete()

			record = BoneChangeRecord()
			record.bone = bone
			record.modifier = request.user
			record.dateChangeMade = datetime.now()
			record.previousReason = "CREATED"
			record.newReason = bone.reason
			record.previousExpirationDate = bone.expirationDate
			record.newExpirationDate = bone.expirationDate

			record.save()

			notify.bone_received(bone)

			request.session['standards_bone_msg'] = "Summons approved. A bone has been levied."
		else:
			request.session['standards_bone_error'] = "Summons failed to be approved: " + str(form.errors)

		return redirect(edit_bones)
	else:
		return redirect(edit_bones)

@permission_required('Standards.delete_summons', login_url='PubSite.views.permission_denied')
def reject_summons(request, summons):
	"""
		Reject a summons.
	"""
	if request.method == 'POST':
		try:
			summons_obj = Summons.objects.get(pk=summons)
		except:
			request.session['standards_bone_error'] = "Sorry, that summons no longer exists. It may have been approved or rejected already."
			return redirect(edit_bones)

		try:
			rejectReason = request.POST["reason"]
		except:
			request.session['standards_bone_error'] = "Unknown error occurred while rejecting summons. Try again later. If the error persists, please contact the Web Chair."
			return redirect(edit_bones)

		summonsHistory = SummonsHistoryRecord()
		summonsHistory.summonee = summons_obj.summonee
		summonsHistory.summoner = summons_obj.summoner
		summonsHistory.details = summons_obj.reason
		summonsHistory.resultReason = rejectReason
		summonsHistory.date = datetime.now()
		summonsHistory.hasBone = False
		summonsHistory.boneID = 0
		summonsHistory.save()

		summons_obj.delete()
		request.session['standards_bone_msg'] = "Summons rejected successfully."

		return redirect(edit_bones)
	else:
		return redirect(edit_bones)

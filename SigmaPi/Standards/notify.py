"""
	Utility functions for notifying users about Standards events
"""
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail, EmailMessage

def summons_requested(summonsRequestCount):
	subject = "Standards Board: New Summons Request(s) Submitted"
	message = str(summonsRequestCount) + " new summons request(s) have been submitted for your approval."
	message = message + " You may view details on the request and approve/deny it at: https://sigmapigammaiota.org/secure/standards/summons/"

	try:
		fourth = User.objects.get(groups__name='4th Counselor')

		send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [fourth.email])
	except:
		pass

def summons_request_denied(summonsRequest):
	subject = "Standards Board: Summons Request Denied"
	message = "Your request to summons " + summonsRequest.summonee.first_name + " " + summonsRequest.summonee.last_name
	message = message + " has been denied. If you want more details, please speak with the Fourth Counselor."

	try:
		fourth = User.objects.get(groups__name='4th Counselor')

		email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
            to=[summonsRequest.summoner.email], cc=[fourth.email])
		
		email.send()
	except:
		pass

def summons_sent(summons):
	subject = "Standards Board: Summons"
	message = "Date: " + summons.dateSummonsSent.strftime("%Y-%m-%d") + ". "
	message = message + "You are receiving this email because you are being summoned."
	if summons.spokeWith:
		message = message + " The recorded outcome of your conversation with the summonee (" +\
		          summons.summonee.last_name + ", " + summons.summonee.first_name + ") is: "
		message = message + summons.outcomes
		message = message + ". The summonee has requested this case be sent to Standards Board for the following reason: " + summons.standards_action
		message = message + "."
	else:
		message = message + " The reason for your summon is as follows: " + summons.special_circumstance + "."
	message = message + " If you feel that you are being unfairly sanctioned, you may attend the next Standards Board meeting to dispute the summon."
	message = message + " If you plan to attend, please notify standards-sigmapi@wpi.edu. If you do not attend, you will automatically be given a punishment by standards."

	try:
		fourth = User.objects.get(groups__name='4th Counselor')
		standards = User.objects.get(groups__name='Parliamentarian')

		email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
            to=[summons.summonee.email], cc=[fourth.email, standards.email, settings.EC_EMAIL])
		
		email.send()
	except:
		pass

def points_requested():
	subject = "Standards Board: New Pi Points Request"
	message = "A new Pi Points request has been submitted for your approval."
	message = message + " You may view the details of the request and approve/deny it at: https://sigmapigammaiota.org/secure/standards/points/"

	try:
		standards = User.objects.get(groups__name='Parliamentarian')

		send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [standards.email])
	except:
		pass

def job_requested(jobRequest):

	if jobRequest.takingJob:
		subject = "Standards Board: House Job Cover Offer"
		message = jobRequest.requester.first_name + " " + jobRequest.requester.last_name
		message = message + " has offered to cover a " + jobRequest.get_job_display() + "."
		message = message + " If you have enough Pi Points and would like to have him cover your job, you can do so at: https://sigmapigammaiota.org/secure/standards/overview/"
	else:
		subject = "Standards Board: House Job Cover Request"
		message = jobRequest.requester.first_name + " " + jobRequest.requester.last_name
		message = message + " needs somebody to cover a " + jobRequest.get_job_display() + "."
		message = message + " If you would like to cover his job, you can do so at: https://sigmapigammaiota.org/secure/standards/overview/."
		message = message + " You will receive Pi Points for covering the job."

	try:
		email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ACTIVES_EMAIL], cc=[jobRequest.requester.email])
		
		email.send()
	except:
		pass

def alertAboutJob(giverRecord, takerUser, jobTitle, jobDetails):
	takerName = takerUser.first_name + " " + takerUser.last_name
	giverName = giverRecord.brother.first_name + " " + giverRecord.brother.last_name
	subject_to_giver = takerName + " has taken your job: " + jobTitle + "!"
	message_to_giver = takerName + " has volunteered to perform your job: " + jobTitle + "."
	message_to_giver = message_to_giver + " Please coordinate with him so that you may ensure the job is"
	message_to_giver = message_to_giver + " completed correctly and on time.  Thank you from the Standards Board."

	subject_to_taker = "You have been assigned to take " + giverName +"'s job: " + jobTitle + "!"
	message_to_taker = "Please ensure that you complete the job correctly and on time.  Failure to do so"
	message_to_taker = message_to_taker + " may result in a loss of Pi Points and/or a summons.  Please "
	message_to_taker = message_to_taker + "coordinate with " + giverName + " concerning the details of the job."
	message_to_taker = message_to_taker + " Thank you from the Standards Board."

	try:
		send_mail(subject_to_giver, message_to_giver, settings.DEFAULT_FROM_EMAIL, [giverRecord.brother.email])
		send_mail(subject_to_taker, message_to_taker, settings.DEFAULT_FROM_EMAIL, [takerUser.email])
	except:
		pass

def bone_received(bone):
	subject = "Standards Board: Bone Received"
	message = "Date Received: " + bone.dateReceived.strftime("%Y-%m-%d") + ". "
	message = message + "Expiration Date: " + bone.expirationDate.strftime("%Y-%m-%d") + ". "
	message = message + "You are receiving this email because you have received a bone."
	message = message + " The reason for your bone is as follows: " + bone.reason + "."
	message = message + " You may view more details on this bone at: https://sigmapigammaiota.org/secure/standards/overview/."

	try:
		fourth = User.objects.get(groups__name='4th Counselor')
		standards = User.objects.get(groups__name='Parliamentarian')

		email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
            to=[bone.bonee.email], cc=[fourth.email, standards.email, settings.EC_EMAIL])
		
		email.send()
	except:
		pass

def probation_received(probation):
	subject = "Standards Board: Social Probation"
	message = "Date Received: " + probation.dateReceived.strftime("%Y-%m-%d") + ". "
	message = message + "Expiration Date: " + probation.expirationDate.strftime("%Y-%m-%d") + ". "
	message = message + "You are receiving this email because you have been put on social probation."

	try:
		standards = User.objects.get(groups__name='Parliamentarian')

		email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
            to=[probation.recipient.email], cc=[standards.email, settings.EC_EMAIL])
		
		email.send()
	except:
		pass

def bone_changed(bone):
	subject = "Standards Board: Bone Changed"
	message = "You are receiving this email because a bone that you received has been changed. The new details of the bone are: "
	message = message + "Expiration Date: " + bone.expirationDate.strftime("%Y-%m-%d") + ". "
	message = message + "Reason: " + bone.reason + ". " 
	message = message + "Pi Point Value: " + str(bone.value) + ". "

	try:
		standards = User.objects.get(groups__name='Parliamentarian')

		email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
            to=[bone.bonee.email], cc=[standards.email, settings.EC_EMAIL])
		
		email.send()
	except:
		pass

def points_changed(changeRecord):
	subject = "Standards Board: Pi Points Changed"
	message = "You are receiving this email because the number of Pi Points you have has changed."
	message = message + "Old Points Value: " + str(changeRecord.oldValue) + ". "
	message = message + "New Points Value: " + str(changeRecord.newValue) + ". " 

	try:
		standards = User.objects.get(groups__name='Parliamentarian')

		email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
            to=[changeRecord.brother.brother.email], cc=[standards.email])
		
		email.send()
	except:
		pass

def point_request_denied(pointRequest):
	subject = "Standards Board: Pi Points Request Denied"
	message = "You are receiving this email because your Pi Points request was denied. If you want more information, please speak with the Parliamentarian"
	
	try:
		standards = User.objects.get(groups__name='Parliamentarian')

		email = EmailMessage(subject=subject, body=message, from_email=settings.DEFAULT_FROM_EMAIL,
            to=[pointRequest.requester.email], cc=[standards.email])
		
		email.send()
	except:
		pass
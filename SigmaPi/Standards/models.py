from django.db import models
from django.contrib.auth.models import User

class Bone(models.Model):
	"""
		Model for a single bone that is given to a User
	"""
	bonee = models.ForeignKey(User, related_name='+')
	boner = models.ForeignKey(User, related_name='+')
	reason = models.TextField()
	dateReceived = models.DateField()
	expirationDate = models.DateField()
	value = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.reason

	def __str__(self):
		return self.reason

	class Meta:
		verbose_name = "Bone"
		verbose_name_plural = "Bones"

class BoneChangeRecord(models.Model):
	"""
		Model for a bone change history record
	"""
	bone = models.ForeignKey(Bone)
	modifier = models.ForeignKey(User, related_name='+')
	dateChangeMade = models.DateTimeField()
	previousReason = models.TextField()
	newReason = models.TextField()
	previousExpirationDate = models.DateField()
	newExpirationDate = models.DateField()

	def __unicode__(self):
		return self.bone

	def __str__(self):
		return self.bone

	class Meta:
		verbose_name = "Bone Change Record"
		verbose_name_plural = "Bone Change Records"


class Probation(models.Model):
	"""
		Model for a probation punishment that a user will receive.
	"""
	recipient = models.ForeignKey(User, related_name='+')
	giver = models.ForeignKey(User, related_name='+')
	dateReceived = models.DateField()
	expirationDate = models.DateField()

	def __unicode__(self):
		return self.recipient

	def __str__(self):
		return self.recipient

	class Meta:
		verbose_name = "Probation"
		verbose_name_plural = "Probations"

class PiPointsRecord(models.Model):
	"""
		Model for a pipoint record for a user
	"""
	brother = models.OneToOneField(User, primary_key=True)
	jobsTaken = models.PositiveIntegerField(default=0)
	points = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.user

	def __str__(self):
		return self.user

	class Meta:
		verbose_name = "Pi Points Record"
		verbose_name_plural = "Pi Points Records"

class PiPointsChangeRecord(models.Model):
	"""
		Model for a PiPoint change history record
	"""
	brother = models.ForeignKey(PiPointsRecord)
	modifier = models.ForeignKey(User, related_name='+')
	dateChanged = models.DateTimeField()
	oldValue = models.PositiveIntegerField(default=0)
	newValue = models.PositiveIntegerField(default=0)

	def __unicode__(self):
		return self.dateChanged

	def __str__(self):
		return self.dateChanged

	class Meta:
		verbose_name = "Pi Points Change Record"
		verbose_name_plural = "Pi Points Change Records"

class PiPointsRequest(models.Model):
	"""
		Model for a request for pi points
	"""
	REASON_CHOICES = (
			('P', 'Pre/Post Party Job'),
			('F', 'First Shift Party Job'),
			('S', 'Second Shift Party Job'),
			('H', 'House Job'),
			('M', 'Meal Crew')
			)

	REASON_POINTS = { 'P': 10, 'F': 30, 'S': 40, 'H': 20, 'M': 20,}

	requester = models.ForeignKey(User, related_name='+')
	date = models.DateTimeField()
	reason = models.TextField(max_length=1, choices=REASON_CHOICES)
	witness = models.CharField(max_length=100, default="None")

	def pointsForReason(self, reason):
		return self.REASON_POINTS[reason]

	def __unicode__(self):
		return self.requester

	def __str__(self):
		return self.requester

	class Meta:
		verbose_name = "Pi Points Request"
		verbose_name_plural = "Pi Points Request"

class JobRequest(models.Model):
	REASON_CHOICES = (
				('P', 'Pre/Post Party Job (10)'),
				('F', 'First Shift Party Job (30)'),
				('S', 'Second Shift Party Job (40)'),
				('H', 'House Job (20)'),
				('M', 'Meal Crew (20)')
				)

	REASON_POINTS = { 'P': 10, 'F': 30, 'S': 40, 'H': 20, 'M': 20,}

	requester = models.ForeignKey(User, related_name='+')
	date = models.DateTimeField()
	job = models.TextField(max_length=1, choices=REASON_CHOICES)
	details = models.TextField()
	takingJob = models.BooleanField(default=False)

	def pointsForReason(self, reason):
		return self.REASON_POINTS[job]

	def __unicode__(self):
		return self.requester

	def __str__(self):
		return self.requester

	class Meta:
		verbose_name = "Job Request"
		verbose_name_plural = "Job Requests"

class SummonsRequest(models.Model):
	"""
		Model for a request to summons a user.
	"""

	summoner = models.ForeignKey(User, related_name='+')
	summonee = models.ForeignKey(User, related_name='+')
	reason = models.TextField()
	dateRequestSent = models.DateField()

	def __unicode__(self):
		return summoner + " wants to summon " + summonee + " for " + self.reason

	def __str__(self):
		return summoner + " wants to summon " + summonee + " for " + self.reason

	class Meta:
		verbose_name = "Summons Request"
		verbose_name_plural = "Summons Requests"

class Summons(models.Model):
	"""
		Model for a summons that is given to a User.
	"""
	summoner = models.ForeignKey(User, related_name='+')
	summonee = models.ForeignKey(User, related_name='+')
	approver = models.ForeignKey(User, related_name='+')
	reason = models.TextField()
	dateSummonsSent = models.DateField()

	def __unicode__(self):
		return summoner + " has summoned " + summonee + " for " + self.reason

	def __str__(self):
		return summoner + " has summoned " + summonee + " for " + self.reason

	class Meta:
		verbose_name = "Summons"
		verbose_name_plural = "Summonses"

class SummonsHistoryRecord(models.Model):
	"""
		Model for a summons history record.
	"""
	summoner = models.ForeignKey(User, related_name='+')
	summonee = models.ForeignKey(User, related_name='+')
	details = models.TextField()
	resultReason = models.TextField()
	date = models.DateField()
	hasBone = models.BooleanField(default=False)
	boneID = models.PositiveIntegerField()



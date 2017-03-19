from django.contrib.auth.models import User
from django.db import models


class SummonsRequest(models.Model):
	"""
		Model for a request to summons a user.
	"""

	summoner = models.ForeignKey(User, related_name='+')
	summonee = models.ForeignKey(User, related_name='+')
	spokeWith = models.BooleanField()
	outcomes = models.TextField(blank=True)
	standards_action = models.TextField(blank=True)
	special_circumstance = models.TextField(blank=True)

	dateRequestSent = models.DateField()

	def reason(self):
		if self.spokeWith:
			return "Conversation outcome: " + self.outcomes + ". Further action required because: " + self.standards_action
		else:
			return self.special_circumstance

	def __unicode__(self):
		return self.summoner.last_name + ", " + self.summoner.first_name + " wants to summon " + self.summonee.last_name + ", " + self.summonee.first_name

	def __str__(self):
		return self.summoner.last_name + ", " + self.summoner.first_name + " wants to summon " + self.summonee.last_name + ", " + self.summonee.first_name

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
	spokeWith = models.BooleanField()
	outcomes = models.TextField(blank=True)
	standards_action = models.TextField(blank=True)
	special_circumstance = models.TextField(blank=True)
	dateSummonsSent = models.DateField()

	def reason(self):
		if self.spokeWith:
			return "Conversation outcome: " + self.outcomes + ". Further action required because: " + self.standards_action
		else:
			return self.special_circumstance

	def __unicode__(self):
		return self.summoner.last_name + ", " + self.summoner.first_name + " has summoned " + self.summonee.last_name + ", " + self.summonee.first_name

	def __str__(self):
		return self.summoner.last_name + ", " + self.summoner.first_name + " has summoned " + self.summonee.last_name + ", " + self.summonee.first_name

	class Meta:
		verbose_name = "Summons"
		verbose_name_plural = "Summonses"


class SummonsHistoryRecord(models.Model):
	"""
		Model for a summons history record.
	"""
	summoner = models.ForeignKey(User, related_name='+')
	summonee = models.ForeignKey(User, related_name='+')
	saved_by = models.ForeignKey(User, related_name='+', null=True)
	details = models.TextField()
	resultReason = models.TextField()
	rejected = models.BooleanField(default=False)
	date = models.DateField()

	def __unicode__(self):
		return self.summoner.last_name + ", " + self.summoner.first_name + " summoned " + self.summonee.last_name + ", " + self.summonee.first_name

	def __str__(self):
		return self.summoner.last_name + ", " + self.summoner.first_name + " summoned " + self.summonee.last_name + ", " + self.summonee.first_name

	class Meta:
		verbose_name = "Summons History Record"
		verbose_name_plural = "Summons History Records"



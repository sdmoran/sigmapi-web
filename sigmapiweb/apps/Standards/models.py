from django.contrib.auth.models import User
from django.db import models

from common.mixins import ModelMixin
from common.utils import get_formal_name_or_deleted


class SummonsRequest(ModelMixin, models.Model):
    """
        Model for a request to summons a user.
    """

    summoner = models.ForeignKey(User, related_name='+', null=True, on_delete=models.SET_NULL)
    summonee = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
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


    def __str__(self):
        return '{0} wants to summon {1}'.format(
            get_formal_name_or_deleted(self.summoner),
            get_formal_name_or_deleted(self.summonee),
        )

    class Meta:
        verbose_name = "Summons Request"
        verbose_name_plural = "Summons Requests"


class Summons(ModelMixin, models.Model):
    """
        Model for a summons that is given to a User.
    """
    summoner = models.ForeignKey(User, related_name='+', null=True, on_delete=models.SET_NULL)
    summonee = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    approver = models.ForeignKey(User, related_name='+', null=True, on_delete=models.SET_NULL)
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

    def __str__(self):
        return '{0} has summoned {1}'.format(
            get_formal_name_or_deleted(self.summoner),
            get_formal_name_or_deleted(self.summonee),
        )

    class Meta:
        verbose_name = "Summons"
        verbose_name_plural = "Summonses"


class SummonsHistoryRecord(ModelMixin, models.Model):
    """
        Model for a summons history record.
    """
    summoner = models.ForeignKey(User, related_name='+', null=True, on_delete=models.SET_NULL)
    summonee = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    saved_by = models.ForeignKey(User, related_name='+', null=True, on_delete=models.SET_NULL)
    details = models.TextField()
    resultReason = models.TextField()
    rejected = models.BooleanField(default=False)
    date = models.DateField()

    def __str__(self):
        return '{0} summoned {1}'.format(
            get_formal_name_or_deleted(self.summoner),
            get_formal_name_or_deleted(self.summonee),
        )

    class Meta:
        verbose_name = "Summons History Record"
        verbose_name_plural = "Summons History Records"


"""
Models for MailingList app.
"""
from django.contrib.auth.models import Group, User
from django.db import models

from common.mixins import ModelMixin


class MailingList(ModelMixin, models.Model):
    """
    A mailing list that can be subscribed to and have invites send to.
    """
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.name


class MailingListAccess(ModelMixin, models.Model):
    """
    Model whose existence indicates that members of the contained
    group have "receive" access to the contained mailing list. If can_send
    is True, the group members can also send to the mailing_list.
    """
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    can_send = models.BooleanField(default=False)

    class Meta:
        unique_together = ('mailing_list', 'group')


class MailingListSubscription(ModelMixin, models.Model):
    """
    A subscription to a mailing list. It is assumed that if this model
    exists, the user has receive access to the mailing list.
    """
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('mailing_list', 'user')

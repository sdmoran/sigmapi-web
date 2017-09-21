"""
Models for MailingList app.
"""
from django.contrib.auth.models import Group, User
from django.db import models

from apps.UserInfo.models import PledgeClass
from common.mixins import ModelMixin

ACCESS_SUBSCRIBE = 'sub'
ACCESS_SEND = 'snd'


# Meta
ACCESS_CHOICE_LEN = 3
ACCESS_DICT = {
    ACCESS_SUBSCRIBE: 'Subscribe',
    ACCESS_SEND: 'Send',
}
ACCESS_CHOICES = tuple(ACCESS_DICT.items())


class MailingList(ModelMixin, models.Model):
    """
    A mailing list that can be subscribed to and have invites send to.
    """
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.name


class GroupMailingListAccess(ModelMixin, models.Model):
    """
    Model granting access to a mailing list to users
    in a specific group.
    """
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    access_type = models.CharField(
        max_length=ACCESS_CHOICE_LEN,
        choices=ACCESS_CHOICES,
        default=ACCESS_SEND,
    )

    class Meta:
        unique_together = ('mailing_list', 'group', 'access_type')


class PledgeClassMailingListAccess(ModelMixin, models.Model):
    """
    Model granting a type of access to a mailing list to users
    in a specific pledge class.
    """
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    pledge_class = models.ForeignKey(PledgeClass, on_delete=models.CASCADE)
    access_type = models.CharField(
        max_length=ACCESS_CHOICE_LEN,
        choices=ACCESS_CHOICES,
        default=ACCESS_SEND,
    )

    class Meta:
        unique_together = ('mailing_list', 'pledge_class', 'access_type')


class ClassYearMailingListAccess(ModelMixin, models.Model):
    """
    Model granting receive and/or send access to a mailing list to users
    in a specific class year.
    """
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    class_year = models.IntegerField(default=2018)
    access_type = models.CharField(
        max_length=ACCESS_CHOICE_LEN,
        choices=ACCESS_CHOICES,
        default=ACCESS_SEND,
    )

    class Meta:
        unique_together = ('mailing_list', 'class_year', 'access_type')


class MailingListSubscription(ModelMixin, models.Model):
    """
    A subscription to a mailing list. It is assumed that if this model
    exists, the user has receive access to the mailing list.
    """
    mailing_list = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('mailing_list', 'user')


class UserLastSentTime(ModelMixin, models.Model):
    """
    Model tracking the last time a user sent an email in order
    to prevent spamming and list loops.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_sent = models.DateTimeField()

    MIN_SECONDS_BETWEEN_SENDS = 15

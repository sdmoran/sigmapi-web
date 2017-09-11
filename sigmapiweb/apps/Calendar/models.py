"""
Models for Calendar app.
"""
from django.contrib.auth.models import Group, User
from django.db import models

from common.mixins import ModelMixin


class Calendar(ModelMixin, models.Model):
    """
    TODO docstring
    """
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=128, default='')

    def __str__(self):
        return self.name


class CalendarAccess(ModelMixin, models.Model):
    """
    TODO docstring
    """
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('calendar', 'group')


class CalendarSubscription(ModelMixin, models.Model):
    """
    TODO docstring
    """
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('calendar', 'user')

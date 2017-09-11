"""
Models for Calendar app.
"""
from django.contrib.auth.models import Group, User
from django.db import models


class Calendar(models.Model):
    """
    TODO docstring
    """
    name = models.CharField(max_length=16, unique=True)
    manager = models.ForeignKey(Group, on_delete=models.CASCADE)


class CalendarAccess(models.Model):
    """
    TODO docstring
    """
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('calendar', 'group')


class CalendarSubscription(models.Model):
    """
    TODO docstring
    """
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('calendar', 'user')

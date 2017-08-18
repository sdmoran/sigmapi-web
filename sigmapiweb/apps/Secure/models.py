"""
Models for the Secure app.
"""
from django.db import models
from django.contrib.auth.models import Group

from common.mixins import ModelMixin


class CalendarKey(ModelMixin, models.Model):
    """
    TODO: Docstring
    """

    # The group which has access to this key.
    group = models.ForeignKey(
        Group,
        related_name="calendar_key",
        default=1,
        on_delete=models.CASCADE
    )

    # The calendar key.
    key = models.CharField(max_length=100)

    def __str__(self):
        return str(self.group) + " " + self.key

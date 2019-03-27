"""
Models for Links app.
"""
from django.contrib.auth.models import User
from django.db import models

from common.mixins import ModelMixin


class Link(ModelMixin, models.Model):
    """
    Model for a single link that a person may submit
    """
    poster = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField()
    title = models.CharField(max_length=50)
    url = models.URLField()
    promoted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
        permissions = (
            ("promote_link", "Can promote links."),
            ("access_link", "Can access links.")
        )

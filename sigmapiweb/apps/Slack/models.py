from django.db import models

from common.mixins import ModelMixin


class CliqueUser(ModelMixin, models.Model):
    """
    Model to act as a substitute for tacking slack users
    Slack usernames can change, but their ID should stay the same.
    We need some sort of unique mapping for the groups to work
    """
    slack_id = models.TextField()

class CliqueGroup(ModelMixin, models.Model):
    """
    Model for keeping track of users in a specific Clique group
    """
    creator = models.ForeignKey(
        CliqueUser,
        on_delete=models.CASCADE,
        related_name="creator",
    )
    name = models.TextField(unique=True)
    members = models.ManyToManyField(CliqueUser)


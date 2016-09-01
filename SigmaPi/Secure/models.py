from django.db import models
from django.contrib.auth.models import Group

class CalendarKey(models.Model):

    # The group which has access to this key.
    group = models.ForeignKey(Group, related_name="calendar_key", default=1)

    # The calendar key.
    key = models.CharField(max_length=100)

    def __unicode__(self):
        return self.group + " " + self.key

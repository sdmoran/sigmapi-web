"""
Models for the Secure app.
"""
import datetime

from django.db import models

from common.mixins import ModelMixin


def timestamp_file_name(fname, fmt='%Y-%m-%d_{fname}'):
    """
    Utility function to add a timestamp to uploaded files.
    """
    return datetime.datetime.now().strftime(fmt).format(fname=fname)


def guidepath(_, filename):
    """
    Path on filesystem where this house guide document should be stored.
    """
    return "protected/guides/" + timestamp_file_name(filename)


def bylaws_path(_, filename):
    """
    Path on filesystem where this bylaws document should be stored.
    """
    return "protected/bylaws/" + timestamp_file_name(filename)


def houserules_path(_, filename):
    """
    Path on filesystem where this house rules document should be stored.
    """
    return "protected/houserules/" + timestamp_file_name(filename)


class Bylaws(ModelMixin, models.Model):
    """
    Model for a single document of house bylaws.
    """
    date = models.DateField()
    filepath = models.FileField(upload_to=bylaws_path)

    def __str__(self):
        return self.date.__str__()

    # Meta information about this model.
    class Meta:
        verbose_name_plural = "Bylaws"
        verbose_name = "Bylaws"
        permissions = (
            ("access_bylaws", "Can access bylaws."),
        )


class HouseRules(ModelMixin, models.Model):
    """
    Model for a single document of house rules.
    """
    date = models.DateField()
    filepath = models.FileField(upload_to=houserules_path)

    def __str__(self):
        return self.date.__str__()

    # Meta information about this model.
    class Meta:
        verbose_name_plural = "House Rules"
        verbose_name = "House Rules"
        permissions = (
            ("access_houserules", "Can access house rules."),
        )


class Guide(ModelMixin, models.Model):
    """
    Model for a single document of a house guide.
    """
    name = models.CharField(max_length=100)
    datePosted = models.DateField()
    description = models.TextField(blank=True)
    filepath = models.FileField(upload_to=guidepath)
    path = models.SlugField(max_length=15)

    def __str__(self):
        return self.name

    # Meta information about this model.
    class Meta:
        verbose_name_plural = "Guides"
        verbose_name = "Guide"
        permissions = (
            ("access_guide", "Can access guides."),
        )

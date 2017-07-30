from django.db import models
from django.forms import ModelForm
from django import forms
import datetime

def timeStamped(fname, fmt='%Y-%m-%d_{fname}'):
    """
        Utility function to add a timestamp to uploaded files.
    """

    return datetime.datetime.now().strftime(fmt).format(fname=fname)

def guidepath(_, filename):
    """
        Path on filesystem where this house guide document should be stored.
    """
    return "protected/guides/" + timeStamped(filename)


def bylaws_path(_, filename):
    """
        Path on filesystem where this bylaws document should be stored.
    """
    return "protected/bylaws/" + timeStamped(filename)

def houserules_path(filename):
    """
        Path on filesystem where this house rules document should be stored.
    """
    return "protected/houserules/" + timeStamped(filename)


class Bylaws(models.Model):
    """
        Model for a single document of house bylaws.
    """


    def __unicode__(self):
        return self.date.__str__()

    def __str__(self):
        return self.date.__str__()

    # Fields for this model.
    date = models.DateField()
    filepath = models.FileField(upload_to=bylaws_path)

    # Meta information about this model.
    class Meta:
        verbose_name_plural = "Bylaws"
        verbose_name = "Bylaws"
        permissions = (
            ("access_bylaws", "Can access bylaws."),
        )


class BylawsForm(ModelForm):
    """
        Model-driven form for adding a bylaws document.
    """

    filepath = forms.FileField()

    # Meta information about this form.
    class Meta:
        model = Bylaws
        exclude = ['date']


class HouseRules(models.Model):
    """
        Model for a single document of house rules.
    """

    def __unicode__(self):
        return self.date.__str__()

    def __str__(self):
        return self.date.__str__()

    # Fields for this model.
    date = models.DateField()
    filepath = models.FileField(upload_to=houserules_path)

    # Meta information about this model.
    class Meta:
        verbose_name_plural = "House Rules"
        verbose_name = "House Rules"
        permissions = (
            ("access_houserules", "Can access house rules."),
        )


class HouseRulesForm(ModelForm):
    """
        Model-driven form for adding a house rules document.
    """

    filepath = forms.FileField()

    # Meta information about this form.
    class Meta:
        model = HouseRules
        exclude = ['date']

class Guide(models.Model):
    """
        Model for a single document of a house guide.
    """

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    # Fields for this model.
    name = models.CharField(max_length=100)
    datePosted = models.DateField()
    description = models.TextField(blank=True)
    filepath = models.FileField(upload_to=guidepath)
    path = models.SlugField(max_length=15)

    # Meta information about this model.
    class Meta:
        verbose_name_plural = "Guides"
        verbose_name = "Guide"
        permissions = (
            ("access_guide", "Can access guides."),
        )


class GuideForm(ModelForm):
    """
        Model-driven form for adding a house guide document.
    """

    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    filepath = forms.FileField()

    # Meta information about this form.
    class Meta:
        model = Guide
        exclude = ['path', 'datePosted']


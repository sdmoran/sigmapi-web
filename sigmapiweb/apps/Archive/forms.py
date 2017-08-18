"""
Forms for the Archive app.
"""
from django import forms
from django.forms import ModelForm

from .models import Bylaws, Guide, HouseRules


class BylawsForm(ModelForm):
    """
    Model-driven form for adding a bylaws document.
    """
    filepath = forms.FileField()

    # Meta information about this form.
    class Meta:
        model = Bylaws
        exclude = ['date']


class HouseRulesForm(ModelForm):
    """
    Model-driven form for adding a house rules document.
    """
    filepath = forms.FileField()

    # Meta information about this form.
    class Meta:
        model = HouseRules
        exclude = ['date']


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

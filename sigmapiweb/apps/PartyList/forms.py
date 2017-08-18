"""
Forms for PartyList app.
"""
from django import forms
from django.forms import ModelForm

from .models import BlacklistedGuest, Guest, Party


class GuestForm(ModelForm):
    """
    Form for adding a guest on the client.
    """
    name = forms.CharField(max_length=100)
    gender = forms.CharField(max_length=10)

    class Meta:
        model = Guest
        fields = ['name', 'gender']


class PartyForm(ModelForm):
    """
    Form for adding a party on the client.
    """
    name = forms.CharField(max_length=100)
    date = forms.DateField()

    class Meta:
        model = Party
        fields = ['name', 'date']


class BlacklistForm(ModelForm):
    """
    Form for adding a guest to the blacklist.
    """
    name = forms.CharField(max_length=100, label='Full Name')
    details = forms.CharField(max_length=1000, label='Details', required=False)

    class Meta:
        model = BlacklistedGuest
        fields = ['name', 'details']


class EditPartyInfoForm(ModelForm):
    """
    Form for editing a party
    """
    name = forms.CharField(max_length=100)
    date = forms.DateField()
    jobs = forms.FileField(required=False)

    class Meta:
        model = Party
        fields = ['name', 'date', 'jobs']

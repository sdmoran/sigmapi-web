"""
Forms for UserInfo app.
"""
from django import forms
from django.forms import ModelForm

from .models import PledgeClass, UserInfo


class EditUserInfoForm(ModelForm):
    """
    Form for editing a user
    """
    phoneNumber = forms.CharField(max_length=100, required=False)
    major = forms.CharField(max_length=100, required=False)
    hometown = forms.CharField(max_length=100, required=False)
    activities = forms.CharField(widget=forms.Textarea, required=False)
    interests = forms.CharField(widget=forms.Textarea, required=False)
    favoriteMemory = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = UserInfo
        fields = ['phoneNumber', 'major', 'hometown', 'activities',
                  'interests', 'favoriteMemory', 'pledgeClass']

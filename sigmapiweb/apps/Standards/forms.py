"""
Forms for Standards app.
"""
from django import forms
from django.contrib.auth.models import User

from .models import SummonsRequest, SummonsHistoryRecord


class CustomModelChoiceField(forms.ModelChoiceField):
    """
    Custom choice field for User models that displays as last_name, first_name.
    """
    def label_from_instance(self, obj):
        """
        Get label for choice field.

        Overrides from ModelChoiceField.
        """
        return obj.last_name + ", " + obj.first_name


class SummonsRequestForm(forms.ModelForm):
    """
    Form for sending a summons request.
    """
    spokeWith = forms.ChoiceField(
        choices=(('yes', 'Yes'), ('no', 'No')),
        widget=forms.RadioSelect()
    )
    outcomes = forms.CharField(widget=forms.Textarea)
    standards_action = forms.CharField(widget=forms.Textarea)
    special_circumstance = forms.CharField(widget=forms.Textarea)
    summonee = CustomModelChoiceField(
        queryset=User.objects.all().order_by(
            'last_name'
        ).exclude(
            groups__name='Alumni'
        )
    )

    class Meta:
        model = SummonsRequest
        exclude = ['summoner', 'dateRequestSent']


class ArchiveSummonsForm(forms.ModelForm):
    """
    Form for archiving a summons.
    """
    details = forms.CharField(widget=forms.Textarea)
    resultReason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = SummonsHistoryRecord
        exclude = ['summoner', 'summonee', 'saved_by', 'date']

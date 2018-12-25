"""
Forms for Scholarship app.
"""
from django import forms
from django.contrib.auth.models import User

from .models import (
    AcademicResource,
    LibraryItem,
    StudyHoursRecord,
    TrackedUser
)


class CustomModelChoiceField(forms.ModelChoiceField):
    """
    TODO: Docstring.
    """

    def label_from_instance(self, obj):
        """
        TODO: Docstring.
        """
        return obj.first_name + " " + obj.last_name


class TrackedUserForm(forms.ModelForm):
    """
    Form for the TrackedUser model.
    """
    user = CustomModelChoiceField(
        queryset=User.objects.all().order_by(
            'last_name'
        ).exclude(
            groups__name='Alumni'
        )
    )
    number_of_hours = forms.IntegerField(min_value=0)

    class Meta:
        model = TrackedUser
        fields = ['user', 'number_of_hours']


class StudyHoursRecordForm(forms.ModelForm):
    """
    Form for a StudyHoursRecord model.
    """
    date = forms.DateField()
    number_of_hours = forms.IntegerField(min_value=1)

    class Meta:
        model = StudyHoursRecord
        fields = ['date', 'number_of_hours']


class AcademicResourceForm(forms.ModelForm):
    """
    Form for an AcademicResource model.
    """
    year = forms.IntegerField(min_value=1)

    resource_pdf = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = AcademicResource
        fields = [
            'course_number', 'professor_name',
            'resource_pdf', 'year', 'term'
        ]


class LibraryItemForm(forms.ModelForm):
    """
    Form for a LibraryItem model.
    """
    class Meta:
        model = LibraryItem
        fields = ['title', 'isbn_number', 'course', 'edition', 'item_pdf']

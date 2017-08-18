"""
Forms for Links app.
"""
from django import forms
from django.forms import ModelForm

from .models import Link


class LinkForm(ModelForm):
    """
    Form for adding a link
    """
    title = forms.CharField(max_length=50)
    url = forms.URLField(max_length=200)
    promoted = forms.BooleanField(required=False)

    class Meta:
        model = Link
        exclude = ['poster', 'date', 'likeCount', 'commentCount']

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

class Link(models.Model):
    """
        Model for a single link that a person may submit
    """

    poster = models.ForeignKey(User)
    date = models.DateTimeField()
    title = models.CharField(max_length=50)
    url = models.URLField()
    promoted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Link"
        verbose_name_plural = "Links"
        permissions = (
            ("promote_link", "Can promote links."),
            ("access_link", "Can access links."),
        )

class LinkForm(ModelForm):
    """
        Form for adding a link
    """

    title = forms.CharField(max_length = 50)
    url = forms.URLField(max_length=200)
    promoted = forms.BooleanField(required=False)

    class Meta:
        model = Link
        exclude = ['poster', 'date', 'likeCount', 'commentCount']





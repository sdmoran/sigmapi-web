from django.db import models
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

from common.mixins import ModelMixin


def filepath(self, filename):
    """
        Defines where files uploaded by the user should be stored
    """
    return "users/" + self.user.username + "/" + filename

class PledgeClass(ModelMixin, models.Model):
    """
        Model for user pledge class relationship.
    """

    name = models.CharField(max_length=100, default="Lambda")
    dateInitiated = models.DateField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Pledge Classes"
        verbose_name = "Pledge Class"
        ordering = ['dateInitiated']

class UserInfo(ModelMixin, models.Model):
    """
        Model for site-specific user info.
        Complements the built in User models
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.FileField(upload_to=filepath, null=True, blank=True)
    phoneNumber = models.CharField(default="", max_length=100, blank=True)
    graduationYear = models.PositiveIntegerField(default=2020)
    major = models.CharField(max_length=100, blank=True)
    hometown = models.CharField(max_length=100, blank=True)
    activities = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    favoriteMemory = models.TextField(blank=True)
    bigBrother = models.ForeignKey(User, related_name="big_brother", default=None, null=True, on_delete=models.SET_DEFAULT)
    pledgeClass = models.ForeignKey(PledgeClass, default=1, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Info"
        verbose_name = "User Info"
        permissions = (
            ("manage_users", "Can manage users."),
            )


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
    pledgeClass = forms.ModelChoiceField(
        queryset=PledgeClass.objects.all(), widget=forms.Select,
        empty_label=None
    )

    class Meta:
        model = UserInfo
        exclude = ['picture', 'graduationYear', 'user', 'bigBrother']

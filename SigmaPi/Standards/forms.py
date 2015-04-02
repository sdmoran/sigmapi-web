from django.contrib.auth.models import User
from django import forms
from django.db import models

from Standards.models import JobRequest, PiPointsRequest, Bone, Probation, Summons, SummonsRequest

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.last_name + ", " + obj.first_name


class JobRequestForm(forms.ModelForm):
  """
    Form for requesting someone take/to take a job
  """
  REASON_CHOICES = (
        ('P', 'Pre/Post Party Job (10)'),
        ('F', 'First Shift Party Job (30)'),
        ('S', 'Second Shift Party Job (40)'),
        ('H', 'House Job (20)'),
        ('M', 'Meal Crew (20)')
        )
  REASON_POINTS = { 'P': 10, 'F': 30, 'S': 40, 'H': 20, 'M': 20,}

  job = forms.ChoiceField(choices=REASON_CHOICES)
  details = models.TextField()

  class Meta:
    model = JobRequest
    exclude = ['requester', 'takingJob', 'date']

class PiPointsRequestForm(forms.ModelForm):
  """
    Form for requesting pipoints
  """
  REASON_CHOICES = (
      ('P', 'Pre/Post Party Job'),
      ('F', 'First Shift Party Job'),
      ('S', 'Second Shift Party Job'),
      ('H', 'House Job'),
      ('M', 'Meal Crew')
      )
  reason = forms.ChoiceField(choices=REASON_CHOICES)
  witness = forms.CharField(max_length=100, required=False)

  class Meta:
    model = PiPointsRequest
    exclude = ['requester', 'date']

class PiPointsAddBrotherForm(forms.Form):
  """
    Form for adding a brother to the pipoints system.
  """
  brother = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni').exclude(pipointsrecord__isnull=False))
  piPoints = forms.IntegerField()

class BoneGivingForm(forms.ModelForm):
  """
    Form for giving Bones
  """

  REASON_CHOICES = (
        (10, 'Pre/Post Party Job (10)'),
        (20, 'House Job/Meal Crew (20)'),
        (30, 'First Shift Party Job (30)'),
        (40, 'Second Shift Party Job (40)'),
        (50, 'Other (50)'),
        (60, 'Other (60)'),
        (70, 'Other (70)'),
        (80, 'Other (80)'),
        (90, 'Other (90)'),
        (100, 'Other (100)')
        )

  bonee = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni'))
  reason = forms.CharField(widget=forms.Textarea)
  expirationDate = forms.DateField()
  value = forms.ChoiceField(choices=REASON_CHOICES)

  class Meta:
    model = Bone
    exclude = ['boner', 'dateReceived']

class BoneEditingForm(forms.ModelForm):
  """
    Form for editing Bones
  """
  reason = forms.CharField(widget=forms.Textarea)
  expirationDate = forms.DateField()
  value = forms.IntegerField(min_value=0)

  class Meta:
    model = Bone
    exclude = ['bonee', 'boner', 'dateReceived']

class ProbationGivingForm(forms.ModelForm):
  """
    Form for giving probation
  """
  recipient = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni'))
  expirationDate = forms.DateField()

  class Meta:
    model = Probation
    exclude = ['giver', 'dateReceived']

class SummonsRequestForm(forms.ModelForm):
  """
    Form for sending a summons request
  """

  reason = forms.CharField(widget=forms.Textarea)
  summonee = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni'))

  class Meta:
    model = SummonsRequest
    exclude = ['summoner', 'dateRequestSent']

class AddSummonsForm(forms.ModelForm):
  """
    Form for sending a summons
  """

  reason = forms.CharField(widget=forms.Textarea)
  summonee = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni'))
  summoner = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni'))

  class Meta:
    model = Summons
    exclude = ['dateSummonsSent', 'approver']

class AcceptSummonsForm(forms.ModelForm):
  """
    Form for accepting a summons
  """

  REASON_CHOICES = (
    (10, 'Pre/Post Party Job (10)'),
    (20, 'House Job/Meal Crew (20)'),
    (30, 'First Shift Party Job (30)'),
    (40, 'Second Shift Party Job (40)'),
    (50, 'Other (50)'),
    (60, 'Other (60)'),
    (70, 'Other (70)'),
    (80, 'Other (80)'),
    (90, 'Other (90)'),
    (100, 'Other (100)')
  )

  expirationDate = forms.DateField()
  value = forms.ChoiceField(choices=REASON_CHOICES)
  reason = forms.CharField(widget=forms.Textarea)


  class Meta:
    model = Bone
    exclude = ['boner', 'dateReceived', 'bonee']


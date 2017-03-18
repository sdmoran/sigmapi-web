from django import forms
from django.contrib.auth.models import User

from Standards.models import SummonsRequest, SummonsHistoryRecord


class CustomModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.last_name + ", " + obj.first_name



class SummonsRequestForm(forms.ModelForm):
	"""
	  Form for sending a summons request
	"""
	spokeWith = forms.ChoiceField(choices=(('yes', 'Yes'), ('no', 'No')), widget=forms.RadioSelect())
	outcomes = forms.CharField(widget=forms.Textarea)
	standards_action = forms.CharField(widget=forms.Textarea)

	special_circumstance = forms.CharField(widget=forms.Textarea)

	summonee = CustomModelChoiceField(queryset=User.objects.all().order_by('last_name').exclude(groups__name='Alumni'))

	class Meta:
		model = SummonsRequest
		exclude = ['summoner', 'dateRequestSent']


class ArchiveSummonsForm(forms.ModelForm):

	details = forms.CharField(widget=forms.Textarea)
	resultReason = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = SummonsHistoryRecord
		exclude = ['summoner', 'summonee', 'saved_by', 'date']

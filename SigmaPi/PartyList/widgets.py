from django.forms import ModelForm
from PartyList.models import Guest, PartyGuest, Party, BlacklistedGuest
from django import forms

class GuestForm(ModelForm):
	"""a form for adding a guest on the client."""
	name = forms.CharField(max_length=100)
	gender = forms.CharField(max_length=10)

	class Meta:
		model = Guest
		fields = ['name','gender']

	def __init__(self,*args, **kwargs):
		super(GuestForm,self).__init__(*args, **kwargs)
		#do extra stuff here if necessary

class PartyForm(ModelForm):
	"""a form for adding a guest on the client."""
	name = forms.CharField(max_length=100)
	date = forms.DateField()

	class Meta:
		model = Party
		fields = ['name','date']

	def __init__(self,*args, **kwargs):
		super(PartyForm,self).__init__(*args, **kwargs)
		#do extra stuff here if necessary

class BlacklistForm(ModelForm):
	name = forms.CharField(max_length=100, label='Full Name')
	details = forms.CharField(max_length=1000, label='Details', required=False)

	class Meta:
		model = BlacklistedGuest
		fields = ['name','details']

	def __init__(self,*args, **kwargs):
		super(BlacklistForm,self).__init__(*args, **kwargs)


class EditPartyInfoForm(ModelForm):
	"""
		Form for editing a party
	"""
	name = forms.CharField(max_length=100)
	date = forms.DateField()
	jobs = forms.FileField(required=False)

	class Meta:
		model = Party
		fields = ['name','date','jobs']

	def __init__(self,*args, **kwargs):
		super(EditPartyInfoForm,self).__init__(*args, **kwargs)
		#do extra stuff here if necessary
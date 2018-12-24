
from apps.PartyListV2.models import Party, RestrictedGuest
from django import forms
from django.forms import ModelForm, DateTimeField, TimeField,
SplitDateTimeField, FileField


class EditPartyForm(ModelForm):

    party_start = SplitDateTimeField(
        input_date_formats=["%m/%d/%Y", "%Y-%m-%d"],
        input_time_formats=["%I:%M %p"], label="Party Start Date / Time:")
    preparty_start = TimeField(
        input_formats=["%I:%M %p"], label="Preparty Start Time:")
    jobs = FileField(required=False, label="Party Jobs:")

    def clean(self):
        cleaned_data = super().clean()
        preparty_start = cleaned_data.get('preparty_start')
        party_start = cleaned_data.get('party_start')
        has_preparty = cleaned_data.get('has_preparty')

        if preparty_start >= party_start.time() and has_preparty:
            self.add_error('party_start', "Party must start after preparty")
            self.add_error('preparty_start',
                           "Preparty must start before the party")

    class Meta:
        model = Party
        fields = ('name', 'party_start',
                  'has_party_invite_limits', 'max_party_invites',
                  'has_preparty', 'preparty_start',
                  'has_preparty_invite_limits', 'max_preparty_invites',
                  'jobs')
        labels = {
            'max_party_invites': "Max Party Invites:",
            'has_preparty': "Does this event have a pre-party check-in?",
            'max_preparty_invites': "Max Preparty Invites:",
            'has_party_invite_limits': "Does the party have limited invites?",
            'has_preparty_invite_limits':
                "Does the preparty have limited invites?",
        }


class RestrictedGuestForm(ModelForm):
    """
    Form for adding a guest to the blacklist.
    """
    name = forms.CharField(max_length=100, label='Full Name')
    details = forms.CharField(
        max_length=1000,
        label='Identifying Details',
        required=True,
    )
    reason = forms.CharField(
        max_length=1000,
        label='Reason',
        required=True,
    )

    class Meta:
        model = RestrictedGuest
        fields = ['name', 'details', 'reason']

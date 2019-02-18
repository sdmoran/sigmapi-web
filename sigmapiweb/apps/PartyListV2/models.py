""" Models for the PartyList V2 app. """
import json
from datetime import datetime

from Levenshtein._levenshtein import distance
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models

from common.mixins import ModelMixin
from common.utils import get_full_name_or_deleted


def _time_stamp_filename(fname, fmt='%Y-%m-%d_{fname}'):
    """
    Utility function to add a timestamp to names of uploaded files.

    Arguments:
        fname (str)
        fmt (str)

    Returns: str
    """
    return datetime.now().strftime(fmt).format(fname=fname)


# pylint: disable=W0613
def get_party_jobs_path(model_instance, filename):
    """
    Given a party jobs filename, return the relative path to it.

    Arguments:
        model_instance: Instance of Party that this file is being saved to
        filename (str): Name of file

    Returns: str
    """
    return "protected/partyjobs/" + _time_stamp_filename(filename)


class Party(ModelMixin, models.Model):
    """
    Model to represent a party.
    """
    name = models.CharField(max_length=100)

    party_start = models.DateTimeField()
    has_party_invite_limits = models.BooleanField(default=False)
    max_party_invites = models.IntegerField(default=5)

    has_preparty = models.BooleanField(default=False)
    preparty_start = models.TimeField()
    has_preparty_invite_limits = models.BooleanField(default=False)
    max_preparty_invites = models.IntegerField(default=3)

    guycount = models.IntegerField(default=0)
    girlcount = models.IntegerField(default=0)
    guys_ever_signed_in = models.IntegerField(default=0)
    girls_ever_signed_in = models.IntegerField(default=0)

    last_updated = models.DateTimeField(auto_now=True)

    # Used for guest list change tracking
    # Any additions / deletions / modifications will increment the counter
    # of the associated party. This lets the client grab only the changes
    # it doesn't know about yet from the guest list
    guest_update_counter = models.IntegerField(default=0)

    jobs = models.FileField(
        upload_to=get_party_jobs_path,
        blank=True,
        null=True
    )

    admin_display_excluded_fields = (
        'id', 'has_party_invite_limits', 'max_party_invites', 'has_preparty', 'preparty_start',
        'has_preparty_invite_limits', 'max_preparty_invites', 'guycount', 'girlcount', 'guys_ever_signed_in',
        'girls_ever_signed_in', 'last_updated', 'guest_update_counter'
    )

    # Not strictly enforced, but shows a warning
    # to the door when this is reached
    VOUCHING_WARNING = 3

    def __str__(self):
        return self.name

    def is_preparty_mode(self):
        """ Check if party is active and in pre-party. """

        if not self.has_preparty:
            return False
        preparty_start = datetime.combine(
            self.party_start.date(), self.preparty_start)
        return (preparty_start < datetime.now()) and (not self.is_party_mode())

    def is_party_mode(self):
        """ Check if party is active. """

        return self.party_start < datetime.now()

    def is_list_closed(self):
        """ Check if list is closed. """

        return self.is_preparty_mode() or self.is_party_mode()

    def user_reached_preparty_limit(self, user: User):
        """
        Determines if a user has reached their pre-party invite limit
        :param user: The user to check
        :return: True if there is an invite limit and the user has reached it,
                False otherwise
        """
        if user is None:
            raise ValueError("User cannot be None")

        # Find invites we used (excluding ones that use another
        # person's invites)
        invites = PartyGuest.objects.filter(
            party=self,
            added_by=user,
            invite_used__isnull=True,
            has_preparty_access=True
        ).count()

        # Add any invites we gave to other people
        invites += PartyGuest.objects.filter(
            party=self,
            invite_used=user,
            has_preparty_access=True
        ).count()

        return invites >= self.max_preparty_invites and self.has_preparty_invite_limits

    def user_reached_party_limit(self, user: User):
        """
        Determines if a user has reached their party invite limit
        :param user: The user to check
        :return: True if there is an invite limit and the user has reached it,
                False otherwise
        """

        if user is None:
            raise ValueError("User cannot be None")

        # Find invites we used (excluding ones that use another
        # person's invites)
        invites = PartyGuest.objects.filter(
            party=self,
            added_by=user,
            invite_used__isnull=True,
        ).count()

        # Add any invites we gave to other people
        invites += PartyGuest.objects.filter(
            party=self,
            invite_used=user,
        ).count()

        return invites >= self.max_party_invites and self.has_party_invite_limits

    def user_reached_vouching_limit(self, user: User):
        """ Indicate a brother has reached their vouching limit. """

        if user is None:
            raise ValueError("User cannot be None")
        vouches = PartyGuest.objects.filter(
            party=self,
            added_by=user,
            was_vouched_for=True
        ).count()

        return vouches >= Party.VOUCHING_WARNING

    def sign_in(self, party_guest):
        """ Sign guest into party. """

        if party_guest.signed_in is False:
            if party_guest.gender == 'M':
                self.guycount += 1
                if party_guest.ever_signed_in is False:
                    self.guys_ever_signed_in += 1
            else:
                self.girlcount += 1
                if party_guest.ever_signed_in is False:
                    self.girls_ever_signed_in += 1

            party_guest.signed_in = True
            self.create_partycount_entry()

    def sign_out(self, party_guest):
        """ Sign guest out of party. """

        if party_guest.signed_in is True:
            if party_guest.gender == 'M':
                self.guycount -= 1
            else:
                self.girlcount -= 1

            party_guest.signed_in = False
            self.create_partycount_entry()

    def modify_count(self, gender, sign):
        """ Update party count. """

        if gender == "M":
            if sign == "1":
                self.guycount += 1
            elif sign == "-1":
                self.guycount = max(self.guycount-1, 0)
            else:
                return 'Invalid sign (must be 1 or -1)'
        elif gender == "F":
            if sign == "1":
                self.girlcount += 1
            elif sign == "-1":
                self.girlcount = max(self.girlcount-1, 0)
            else:
                return 'Invalid sign (must be 1 or -1)'
        else:
            return 'Invalid gender supplied'

        self.create_partycount_entry()
        return 'Party count updated!'

    def create_partycount_entry(self):
        """
        Create record for the party count.
        """

        PartyCountRecord(
            party=self,
            guycount=self.guycount,
            girlcount=self.girlcount,
            guysever=self.guys_ever_signed_in,
            girlsever=self.girls_ever_signed_in
        ).save()

    def update_timestamp(self):
        """ Update timestamp with current time. """

        self.last_updated = datetime.now()

    def to_json(self):
        """ Convert class object to JSON. """

        count_history = PartyCountRecord.objects.filter(
            party__id=self.id).all()
        return {
            "prepartyMode": self.is_preparty_mode(),
            "partyMode": self.is_party_mode(),
            "guyCount": self.guycount,
            "girlCount": self.girlcount,
            "guysEverSignedIn": self.guys_ever_signed_in,
            "girlsEverSignedIn": self.girls_ever_signed_in,
            "minLevenshteinDist": RestrictedGuest.MIN_LEVENSHTEIN_DIST,
            "hasPrepartyInviteLimits": self.has_preparty_invite_limits,
            "hasPartyInviteLimits": self.has_party_invite_limits,
            "listClosed": self.is_list_closed(),
            "lastUpdated": self.last_updated.timestamp(),
            "guestUpdateCounter": self.guest_update_counter,
            "countHistory": [entry.to_json() for entry in count_history]
        }

    class Meta:
        verbose_name_plural = "Parties"
        verbose_name = "Party"
        permissions = (
            ("view_parties", "Can view the Parties app"),
            ("manage_parties", "Can manage Parties"),
            ("door_access", "Has access to door check-in")
        )
        default_permissions = []


class PartyCountRecord(ModelMixin, models.Model):
    """ Class to keep track of the party count. """

    party = models.ForeignKey(
        Party,
        related_name="related_party",
        default=1,
        on_delete=models.CASCADE,
    )
    guycount = models.IntegerField()
    girlcount = models.IntegerField()
    guysever = models.IntegerField()
    girlsever = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def to_json(self):
        """ Convert class object to JSON. """

        return {
            "guyCount": self.guycount,
            "girlCount": self.girlcount,
            "guysEverSignedIn": self.guysever,
            "girlsEverSignedIn": self.girlsever,
            "timeStamp": self.created_at.isoformat()
        }


class PartyGuestAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PartyGuestAdminForm, self).__init__(*args, **kwargs)

    gender = forms.ChoiceField(widget=forms.Select, choices=(('M', 'Male'), ('F', 'Female')))


class PartyGuest(ModelMixin, models.Model):
    """ Class to represent a party guest. """

    name = models.CharField(max_length=100, db_index=True)
    gender = models.CharField(max_length=5)

    party = models.ForeignKey(
        Party,
        related_name="party_for_guest",
        default=1,
        on_delete=models.CASCADE,
    )

    added_by = models.ForeignKey(
        User,
        related_name="invited_guests",
        null=True,
        blank=False,
        default=None,
        on_delete=models.CASCADE,
    )

    invite_used = models.ForeignKey(
        User,
        related_name="invites_used_for",
        null=True,
        blank=True,
        default=None,
        on_delete=models.CASCADE,
    )

    has_preparty_access = models.BooleanField(default=False)
    was_vouched_for = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    _signed_in = models.BooleanField(default=False, db_column='signedIn')
    ever_signed_in = models.BooleanField(default=False)
    time_first_signed_in = models.DateTimeField(null=True, blank=True,)
    _cached_json = models.TextField(null=True, blank=True)
    update_counter = models.IntegerField(default=0)

    admin_display_excluded_fields = ('id', '_cached_json', 'update_counter')
    admin_search_fields = ('name',)
    admin_form = PartyGuestAdminForm

    def get_cached_json(self):
        """ Get cached party status. """

        if self._cached_json is None or self._cached_json == "":
            self.save()
        return json.loads(self._cached_json)

    cached_json = property(get_cached_json)

    # Defining a property here so we can figure out timestamps
    def get_signed_in(self):
        """ Return signed-in status of guest. """

        return self._signed_in

    def set_signed_in(self, value):
        """ Set guest as signed in. """

        self._signed_in = value
        if value:
            if self.ever_signed_in is False:
                self.ever_signed_in = True
            if not self.time_first_signed_in:
                self.time_first_signed_in = datetime.now()

    signed_in = property(get_signed_in, set_signed_in)

    def invite_used_name(self):
        """ Get guest name. """

        if self.invite_used is not None:
            return self.invite_used.get_full_name()
        return False

    def formatted_time_first_signed_in(self):
        """ Formats the time when a guest is signed in. """

        if self.ever_signed_in:
            return self.time_first_signed_in.strftime("%I:%M %p")
        return None

    # Setup meta info about this model
    class Meta:
        verbose_name_plural = "Party Guests"
        verbose_name = "Party Guest"
        permissions = (
            ("can_destroy_any_party_guest", "Can Remove Any Party Guest"),
            ("add_party_guests", "Can add guests to a Party")
        )
        default_permissions = []

    def save(self, *args, **kwargs):
        """  Update partylist. """

        if self.id is not None:
            self._cached_json = json.dumps(self.to_json())

        if self._cached_json == "":
            self._cached_json = None

        self.party.guest_update_counter += 1
        self.update_counter = self.party.guest_update_counter
        self.party.save()

        super(PartyGuest, self).save(*args, **kwargs)

    def to_json(self):
        """
        Serializes self to a JSON-serializable dict to be passed to client.

        Returns: dict
        """

        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'addedBy': {
                'name': self.added_by.get_full_name(),
                'id': self.added_by.id,
                'username': self.added_by.username,
            },
            'signedIn': self.signed_in,
            'wasVouchedFor': self.was_vouched_for,
            'everSignedIn': self.ever_signed_in,
            'prepartyAccess': self.has_preparty_access,
            'inviteUsed': self.invite_used_name(),
            'timeFirstSignedIn': self.formatted_time_first_signed_in(),
            'createdAt': self.created_at.isoformat()
        }



class RestrictedGuest(ModelMixin, models.Model):
    """
    Model to represent a person who has been blacklisted or graylisted.
    """
    name = models.CharField(max_length=100)
    added_by = models.ForeignKey(
        User,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        default=None,
    )
    details = models.TextField(
        default="(No identifying details provided)"
    )
    reason = models.TextField(default="(No reason provided)")
    graylisted = models.BooleanField(default=False)

    # Used for name comparison (blacklist checking, duplicate checking)
    # https://en.wikipedia.org/wiki/Levenshtein_distance
    MIN_LEVENSHTEIN_DIST: int = 3

    def __str__(self):
        return self.name

    def matches(self, name):
        """
        Determine if name matches restricted guest's name
        """

        return distance(self.name, name) <= RestrictedGuest.MIN_LEVENSHTEIN_DIST

    def to_json(self):
        """
        Return a dictionary form of self.

        Returns: dict
        """
        return {
            'name': self.name,
            'details': self.details,
            'addedBy': get_full_name_or_deleted(self.added_by),
            'reason': self.reason,
            'graylisted': self.graylisted
        }

    def can_be_deleted_by(self, user):
        """
        Determine if graylisted guest can be deleted by current user.
        """

        if self.graylisted:
            return self.added_by == user or user.has_perm("PartyListV2.manage_graylist")
        return user.has_perm("PartyListV2.manage_blacklist")

    class Meta:
        permissions = (
            ("view_restricted_guests", "Can view Restricted Guests"),
            ("manage_blacklist", "Can manage the Blacklist"),
            ("add_graylist", "Can add to the Graylist"),
            ("manage_graylist", "Can manage any Graylisted Guest")
        )
        default_permissions = []


class SearchLogEntry(ModelMixin, models.Model):
    """ Model for search logs. """

    user = models.ForeignKey(
        User,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        default=None,
    )
    party = models.ForeignKey(
        Party,
        related_name="party_for_search",
        default=1,
        on_delete=models.CASCADE,
    )

    search = models.TextField()

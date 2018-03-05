"""
Models for PartyList app.
"""
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from fuzzywuzzy import fuzz

from common.mixins import ModelMixin
from common.utils import get_id_or_sentinel, get_full_name_or_deleted


def _time_stamp_filename(fname, fmt='%Y-%m-%d_{fname}'):
    """
    Utility function to add a timestamp to names of uploaded files.

    Arguments:
        fname (str)
        fmt (str)

    Returns: str
    """
    return datetime.now().strftime(fmt).format(fname=fname)


def get_party_jobs_path(_, filename):
    """
    Given a party jobs filename, return the relative path to it.

    Arguments:
        _ (?): Expected by upload_to
        filename (str): Name of file

    Returns: str
    """
    return "parties/partyjobs/" + _time_stamp_filename(filename)


def user_can_delete_greylisting(user, greylisting):
    """
    Is a user allowed to remove a guest from the greylist?

    Arguments:
        user: User
        greylisting: GreylistedGuest

    Returns: bool
    """
    return (
        greylisting.addedBy == user or
        user.has_perm('PartyList.can_delete_any_greylisted_guest')
    )


class Party(ModelMixin, models.Model):
    """
    Model to represent a party.
    """
    name = models.CharField(max_length=100)
    date = models.DateField()
    guycount = models.IntegerField(default=0)
    girlcount = models.IntegerField(default=0)
    guy_delta = models.IntegerField(default=0)
    girl_delta = models.IntegerField(default=0)
    guys_ever_signed_in = models.IntegerField(default=0)
    girls_ever_signed_in = models.IntegerField(default=0)

    # TODO: In the future, this path should be changed to be in
    # protected file space so it is not accessible to the public.
    jobs = models.FileField(
        upload_to=get_party_jobs_path,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    def is_party_mode(self):
        """
        Return whether the party is in party mode.

        Returns: bool
        """
        close_datetime = datetime(
            self.date.year,
            self.date.month,
            self.date.day,
            20
        )
        return close_datetime < datetime.now()

    class Meta:
        verbose_name_plural = "Parties"
        verbose_name = "Party"
        permissions = (
            ("manage_parties", "Can manage Parties"),
        )


class BlacklistedGuest(ModelMixin, models.Model):
    """
    Model to represent a person who has been blacklisted.

    Does NOT use the Guest model; just simply stores a name and details.
    """
    name = models.CharField(max_length=100, db_index=True)
    details = models.TextField(
        default="(No identifying details provided)"
    )
    reason = models.TextField(default="(No reason provided)")

    MIN_MATCH_RATIO = 70

    def __str__(self):
        return self.name

    def check_match(self, to_check):
        """
        Return int indicating strength of match, where 0 indicates no match.

        Arguments:
            to_check (str)

        Returns: int
        """
        check_name = ''.join(c.lower() for c in to_check if not c.isspace())
        bl_name = ''.join(c.lower() for c in self.name if not c.isspace())
        match_ratio = fuzz.ratio(check_name, bl_name)
        return match_ratio if match_ratio >= self.MIN_MATCH_RATIO else 0

    def to_json(self):
        """
        Return a dictionary form of self.

        Returns: dict
        """
        return {
            'name': self.name,
            'details': self.details,
            'reason': self.reason,
        }

    class Meta:
        permissions = (
            ("manage_blacklist", "Can manage the blacklist"),
        )


class GreylistedGuest(ModelMixin, models.Model):
    """
    Model to represent a person who has been greylisted.

    Does NOT use the Guest model; just simply stores a name and details.
    """
    name = models.CharField(max_length=100, db_index=True)
    addedBy = models.ForeignKey(
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

    MIN_MATCH_RATIO = 70

    def __str__(self):
        return self.name

    def check_match(self, to_check):
        """
        Returns self if it matches the name to_check, else None.

        Arguments:
            to_check (str)

        Returns: (GreylistedGuest|NoneType)s
        """
        check_name = ''.join(c.lower() for c in to_check if not c.isspace())
        gl_name = ''.join(c.lower() for c in self.name if not c.isspace())
        match_ratio = fuzz.ratio(check_name, gl_name)
        return match_ratio if match_ratio >= self.MIN_MATCH_RATIO else 0

    def to_json(self):
        """
        Return a dictionary form of self.

        Returns: dict
        """
        return {
            'name': self.name,
            'addedBy': get_full_name_or_deleted(self.addedBy),
            'details': self.details,
            'reason': self.reason,
        }

    class Meta:
        permissions = (
            (
                'can_delete_any_greylisted_guest',
                'Can delete any greylsted guest',
            ),
        )


class Guest(ModelMixin, models.Model):
    """
    Model to represent a guest, not specific to any party.
    """
    name = models.CharField(max_length=100, db_index=True)
    birthDate = models.DateField(blank=True, auto_now=True)
    gender = models.CharField(max_length=100)
    cardID = models.CharField(max_length=100, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))

    def __cmp__(self, other):
        pass  # Apparently, django does not use this during the order_by query

    # Setup meta info about this model
    class Meta:
        verbose_name_plural = "Guests"
        verbose_name = "Guest"


class PartyGuest(ModelMixin, models.Model):
    """
    Model to represent a guest for a specific party.
    """
    party = models.ForeignKey(
        Party,
        related_name="party_for_guest",
        default=1,
        on_delete=models.CASCADE,
    )
    guest = models.ForeignKey(
        Guest,
        related_name="guest",
        default=1,
        db_index=True,
        on_delete=models.CASCADE,
    )
    addedBy = models.ForeignKey(
        User,
        related_name="added_by",
        null=True,
        blank=False,
        default=None,
        on_delete=models.SET_NULL,
    )
    wasVouchedFor = models.BooleanField()
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    signedIn = models.BooleanField(default=False)
    everSignedIn = models.BooleanField(default=False)
    timeFirstSignedIn = models.DateTimeField(auto_now_add=True)
    potentialBlacklisting = models.ForeignKey(
        BlacklistedGuest,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )
    potentialGreylisting = models.ForeignKey(
        GreylistedGuest,
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.guest.name

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))

    # Setup meta info about this model
    class Meta:
        verbose_name_plural = "Party Guests"
        verbose_name = "Party Guest"
        permissions = (("can_destroy_any_party_guest",
                        "Can Remove Any Party Guest"),)

    def to_json(self):
        """
        Serializes self to a JSON-serializable dict to be passed to client.

        Returns: dict
        """
        data = {}
        data['id'] = self.id
        data['name'] = self.guest.name
        data['addedByName'] = get_full_name_or_deleted(self.addedBy)
        data['addedByID'] = get_id_or_sentinel(self.addedBy)
        data['signedIn'] = self.signedIn
        data['wasVouchedFor'] = self.wasVouchedFor
        data['potentialBlacklisting'] = (
            self.potentialBlacklisting.to_json()
            if self.potentialBlacklisting
            else None
        )
        data['potentialGreylisting'] = (
            self.potentialGreylisting.to_json()
            if self.potentialGreylisting
            else None
        )

        return data

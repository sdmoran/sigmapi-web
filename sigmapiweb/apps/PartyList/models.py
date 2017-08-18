"""
Models for PartyList app.
"""
from datetime import datetime
import editdistance

from django.db import models
from django.contrib.auth.models import User

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
    details = models.TextField()

    MAX_MATCH_EDIT_DISTANCE = 5

    def __str__(self):
        return self.name

    def check_match(self, to_check):
        """
        Returns self if it matches the name to_check, else None.

        Arguments:
            to_check (str)

        Returns: (BlacklistedGuest|NoneType)s
        """
        check_name = ''.join(c.lower() for c in to_check if not c.isspace())
        bl_name = ''.join(c.lower() for c in self.name if not c.isspace())
        edit_distance = editdistance.eval(check_name, bl_name)
        return (
            self
            if edit_distance <= self.MAX_MATCH_EDIT_DISTANCE
            else None
        )

    class Meta:
        permissions = (
            ("manage_blacklist", "Can manage the blacklist"),
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
        default=1,
        null=True,
        on_delete=models.SET_NULL,
    )
    createdAt = models.DateTimeField(auto_now_add=True, db_index=True)
    signedIn = models.BooleanField(default=False)
    everSignedIn = models.BooleanField(default=False)
    timeFirstSignedIn = models.DateTimeField(auto_now_add=True)

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

        return data

    def check_blacklisted(self):
        """
        Return this guest's match on the blacklist if one exists, else None.

        Returns: (BlacklistedGuest|NoneType)
        """
        match_results = (
            blacklisted.check_match(self.guest.name)
            for blacklisted in BlacklistedGuest.objects.all()
        )
        positives = (match for match in match_results if match)
        return positives.next() if positives else None

""" Register your models here. """
from apps.PartyListV2.models import Party, PartyGuest, RestrictedGuest
from common.utils import register_model_admins

register_model_admins(
    Party,
    PartyGuest,
    RestrictedGuest,
)

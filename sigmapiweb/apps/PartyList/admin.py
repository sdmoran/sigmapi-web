"""
Admin config for PartyList app.
"""
from common.utils import register_model_admins

from .models import BlacklistedGuest, Guest, Party, PartyGuest


register_model_admins(
    BlacklistedGuest,
    Guest,
    Party,
    PartyGuest,
)

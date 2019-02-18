"""
Admin config for PartyList app.
"""
from common.utils import register_model_admins

from .models import BlacklistedGuest, GreylistedGuest, Guest, Party, PartyGuest


# register_model_admins(
#     BlacklistedGuest,
#     GreylistedGuest,
#     Guest,
#     Party,
#     PartyGuest,
# )

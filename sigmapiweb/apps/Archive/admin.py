"""
Admin config for Secure app.
"""
from common.utils import register_model_admins

from .models import Bylaws, Guide, HouseRules


register_model_admins(
    Bylaws,
    Guide,
    HouseRules,
)

"""
Admin config for UserInfo app.
"""
from common.utils import register_model_admins

from .models import PledgeClass, UserInfo


register_model_admins(
    PledgeClass,
    UserInfo,
)

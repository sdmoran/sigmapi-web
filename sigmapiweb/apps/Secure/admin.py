"""
Admin config for Secure app.
"""
from common.utils import register_model_admins

from .models import CalendarKey


register_model_admins(
    CalendarKey,
)

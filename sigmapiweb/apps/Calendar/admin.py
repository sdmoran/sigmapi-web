"""
Admin config for Caldnear app.
"""
from common.utils import register_model_admins

from .models import (
    Calendar,
    CalendarAccess,
    CalendarSubscription,
)


register_model_admins(
    Calendar,
    CalendarAccess,
    CalendarSubscription,
)

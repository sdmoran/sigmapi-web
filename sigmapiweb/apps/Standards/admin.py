"""
Admin config for Standards app.
"""
from common.utils import register_model_admins

from .models import Summons, SummonsHistoryRecord, SummonsRequest


register_model_admins(
    Summons,
    SummonsHistoryRecord,
    SummonsRequest,
)

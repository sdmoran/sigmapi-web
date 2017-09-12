"""
Admin config for MailingList app.
"""
from common.utils import register_model_admins

from .models import (
    MailingList,
    MailingListAccess,
    MailingListSubscription,
)


register_model_admins(
    MailingList,
    MailingListAccess,
    MailingListSubscription,
)

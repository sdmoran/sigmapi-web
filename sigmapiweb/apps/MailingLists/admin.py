"""
Admin config for MailingList app.
"""
from common.utils import register_model_admins

from .models import (
    MailingList,
    GroupMailingListAccess,
    PledgeClassMailingListAccess,
    ClassYearMailingListAccess,
    MailingListSubscription,
)


register_model_admins(
    MailingList,
    GroupMailingListAccess,
    PledgeClassMailingListAccess,
    ClassYearMailingListAccess,
    MailingListSubscription,
)

from common.utils import register_model_admin
from .models import Summons, SummonsRequest, SummonsHistoryRecord

# Register models to appear in the Django Admin DB Site
register_model_admin(Summons)
register_model_admin(SummonsRequest)
register_model_admin(SummonsHistoryRecord)

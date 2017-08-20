from common.utils import register_model_admin
from .models import UserInfo, PledgeClass

# Register your models here.
register_model_admin(UserInfo)
register_model_admin(PledgeClass)
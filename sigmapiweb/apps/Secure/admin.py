from common.utils import register_model_admin
from .models import CalendarKey

# Register models to appear in the Django Admin DB Site
register_model_admin(CalendarKey)

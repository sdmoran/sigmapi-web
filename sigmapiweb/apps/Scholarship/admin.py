from common.utils import register_model_admin
from .models import TrackedUser, StudyHoursRecord, AcademicResource, LibraryItem

# Register models to appear in the Django Admin DB Site
register_model_admin(TrackedUser)
register_model_admin(StudyHoursRecord)
register_model_admin(AcademicResource)
register_model_admin(LibraryItem)

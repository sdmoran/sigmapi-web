from django.contrib import admin
from Scholarship.models import TrackedUser, StudyHoursRecord, AcademicResource, LibraryItem

# Register models to appear in the Django Admin DB Site
admin.site.register(TrackedUser)
admin.site.register(StudyHoursRecord)
admin.site.register(AcademicResource)
admin.site.register(LibraryItem)

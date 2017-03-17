from django.contrib import admin
from Standards.models import Summons, SummonsRequest, SummonsHistoryRecord

# Register models to appear in the Django Admin DB Site
admin.site.register(Summons)
admin.site.register(SummonsRequest)
admin.site.register(SummonsHistoryRecord)
admin.site.register(BoneChangeRecord)
admin.site.register(Bone)

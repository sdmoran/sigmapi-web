"""
Admin config for UserInfo app.
"""
from common.utils import register_model_admins
from django.contrib import admin

from .models import PledgeClass, UserInfo

class UserInfoAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name']
    list_display = tuple([
            field.name
            for field in UserInfo._meta.fields
            if field.name not in UserInfo.admin_display_excluded_fields
        ])

admin.site.register(UserInfo, UserInfoAdmin)

register_model_admins(
    PledgeClass,
)

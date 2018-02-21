"""
Admin config for UserInfo app.
"""
from django.contrib import admin
from common.utils import register_model_admins

from .models import PledgeClass, UserInfo


class UserInfoAdmin(admin.ModelAdmin):
    """
    Class to represent the user info for an Admin
    """
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

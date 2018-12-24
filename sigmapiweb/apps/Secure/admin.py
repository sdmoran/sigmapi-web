"""
Admin config for Secure app.
"""
from common.utils import register_model_admins

from .models import CalendarKey
from django.contrib import admin
from django.contrib.admin.models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('content_type',
                       'user',
                       'action_time',
                       'object_id',
                       'object_repr',
                       'action_flag',
                       'change_message'
                       )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(LogEntryAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(LogEntry, LogEntryAdmin)

register_model_admins(
    CalendarKey,
)

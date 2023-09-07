from django.contrib import admin
from .models import ApplicationAuditLog


class ApplicationAuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'object_changed', 'object_type', 'changed_by', 'message']
    list_filter = ('timestamp', 'object_type', 'changed_by')
    readonly_fields = ('timestamp', 'object_changed', 'object_type', 'changed_by', 'message', 'old_value', 'new_value')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(ApplicationAuditLog, ApplicationAuditLogAdmin)

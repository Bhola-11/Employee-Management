from django.contrib import admin
from .models import ActivityLog, ModelChangeLog

class ModelChangeLogInline(admin.TabularInline):
    model = ModelChangeLog
    extra = 0
    readonly_fields = ('field_name', 'old_value', 'new_value')

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'module_name', 'object_repr', 'user', 'organization', 'ip_address', 'created_at')
    search_fields = ('object_repr', 'description', 'user__email', 'ip_address')
    list_filter = ('action_type', 'module_name', 'organization')
    readonly_fields = ('id', 'organization', 'user', 'action_type', 'module_name', 'object_id', 'object_repr', 'description', 'ip_address', 'user_agent', 'changes_json', 'created_at')
    inlines = [ModelChangeLogInline]

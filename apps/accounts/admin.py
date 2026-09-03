from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Permission, RolePermission, UserRoleAssignment, UserSessionLog

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'organization', 'active_role', 'is_org_admin', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('organization', 'is_org_admin', 'is_staff', 'is_superuser')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        ('WorkSphere Access', {'fields': ('organization', 'active_role', 'is_org_admin', 'is_super_admin')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Preferences & Security', {'fields': ('dark_mode', 'preferred_language', 'two_factor_enabled')}),
    )

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_system_role', 'organization')
    search_fields = ('name', 'code')
    list_filter = ('is_system_role',)

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'module', 'action')
    search_fields = ('name', 'code')
    list_filter = ('module', 'action')

admin.site.register(RolePermission)
admin.site.register(UserRoleAssignment)
admin.site.register(UserSessionLog)

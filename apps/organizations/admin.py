from django.contrib import admin
from .models import (
    Organization, Branch, Department, Team, Designation,
    JobLevel, EmploymentType, WorkLocation, ReportingHierarchy
)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'domain', 'currency', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'domain')
    list_filter = ('is_active',)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization', 'city', 'country', 'is_headquarters', 'is_active')
    search_fields = ('name', 'code', 'city')
    list_filter = ('organization', 'is_headquarters', 'is_active')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization', 'branch', 'department_head', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('organization', 'is_active')

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'organization', 'department', 'job_level', 'is_active')
    search_fields = ('title', 'code')
    list_filter = ('organization', 'job_level')

admin.site.register(Team)
admin.site.register(JobLevel)
admin.site.register(EmploymentType)
admin.site.register(WorkLocation)
admin.site.register(ReportingHierarchy)

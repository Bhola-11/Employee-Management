from django.contrib import admin
from .models import (
    Employee, EmergencyContact, EmployeeAddress, EmployeeEducation,
    EmployeePastExperience, SkillCategory, Skill, EmployeeSkill,
    EmployeeBankDetail, EmployeeTaxInfo, EmployeeStatutoryDocument,
    EmployeeLifecycleTransition
)

class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 1

class EmployeeAddressInline(admin.StackedInline):
    model = EmployeeAddress
    extra = 1

class EmployeeBankDetailInline(admin.StackedInline):
    model = EmployeeBankDetail
    extra = 0

class EmployeeTaxInfoInline(admin.StackedInline):
    model = EmployeeTaxInfo
    extra = 0

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'organization', 'department', 'designation', 'employment_status', 'joining_date')
    search_fields = ('employee_id', 'first_name', 'last_name', 'work_email')
    list_filter = ('organization', 'employment_status', 'department', 'branch')
    inlines = [EmergencyContactInline, EmployeeAddressInline, EmployeeBankDetailInline, EmployeeTaxInfoInline]

admin.site.register(SkillCategory)
admin.site.register(Skill)
admin.site.register(EmployeeSkill)
admin.site.register(EmployeeEducation)
admin.site.register(EmployeePastExperience)
admin.site.register(EmployeeStatutoryDocument)
admin.site.register(EmployeeLifecycleTransition)

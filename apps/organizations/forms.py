from django import forms
from .models import (
    Organization, Branch, Department, Team, Designation,
    JobLevel, EmploymentType, WorkLocation, ReportingHierarchy
)

class BaseStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label or field_name.replace('_', ' ').title()

class OrganizationForm(BaseStyledForm):
    class Meta:
        model = Organization
        fields = [
            'name', 'code', 'domain', 'industry', 'tax_id', 'registration_number',
            'email', 'phone', 'website', 'currency', 'timezone', 'date_format',
            'fiscal_year_start', 'max_employees', 'logo', 'is_active'
        ]

class BranchForm(BaseStyledForm):
    class Meta:
        model = Branch
        fields = [
            'name', 'code', 'is_headquarters', 'address_line1', 'address_line2',
            'city', 'state', 'country', 'postal_code', 'phone', 'email', 'timezone', 'is_active'
        ]

class DepartmentForm(BaseStyledForm):
    class Meta:
        model = Department
        fields = [
            'branch', 'name', 'code', 'parent_department', 'department_head',
            'budget', 'description', 'is_active'
        ]

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['branch'].queryset = Branch.objects.filter(organization=org)
            self.fields['parent_department'].queryset = Department.objects.filter(organization=org)
            from apps.employees.models import Employee
            self.fields['department_head'].queryset = Employee.objects.filter(organization=org)

class TeamForm(BaseStyledForm):
    class Meta:
        model = Team
        fields = ['department', 'name', 'code', 'team_lead', 'description', 'is_active']

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['department'].queryset = Department.objects.filter(organization=org)
            from apps.employees.models import Employee
            self.fields['team_lead'].queryset = Employee.objects.filter(organization=org)

class DesignationForm(BaseStyledForm):
    class Meta:
        model = Designation
        fields = ['department', 'job_level', 'title', 'code', 'min_salary', 'max_salary', 'description', 'is_active']

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['department'].queryset = Department.objects.filter(organization=org)
            self.fields['job_level'].queryset = JobLevel.objects.filter(organization=org)

class JobLevelForm(BaseStyledForm):
    class Meta:
        model = JobLevel
        fields = ['level_name', 'rank_order', 'description', 'is_active']

class EmploymentTypeForm(BaseStyledForm):
    class Meta:
        model = EmploymentType
        fields = ['name', 'code', 'standard_hours_per_week', 'has_benefits', 'is_active']

class WorkLocationForm(BaseStyledForm):
    class Meta:
        model = WorkLocation
        fields = ['branch', 'name', 'location_type', 'building', 'floor', 'seating_capacity', 'is_active']

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['branch'].queryset = Branch.objects.filter(organization=org)

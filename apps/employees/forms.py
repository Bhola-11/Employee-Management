from django import forms
from .models import (
    Employee, EmergencyContact, EmployeeAddress, EmployeeEducation,
    EmployeePastExperience, EmployeeSkill, EmployeeBankDetail,
    EmployeeTaxInfo, EmployeeStatutoryDocument, EmployeeLifecycleTransition
)
from apps.organizations.models import Branch, Department, Designation, JobLevel, EmploymentType, WorkLocation, Team

class BaseStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['type'] = 'date'
            else:
                field.widget.attrs['class'] = 'form-control'

class EmployeeCreateForm(BaseStyledForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'middle_name', 'last_name', 'gender',
            'date_of_birth', 'marital_status', 'blood_group', 'personal_email',
            'work_email', 'phone_number', 'branch', 'department', 'designation',
            'job_level', 'employment_type', 'work_location', 'team',
            'direct_manager', 'joining_date', 'employment_status', 'profile_photo', 'biography'
        ]

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['branch'].queryset = Branch.objects.filter(organization=org)
            self.fields['department'].queryset = Department.objects.filter(organization=org)
            self.fields['designation'].queryset = Designation.objects.filter(organization=org)
            self.fields['job_level'].queryset = JobLevel.objects.filter(organization=org)
            self.fields['employment_type'].queryset = EmploymentType.objects.filter(organization=org)
            self.fields['work_location'].queryset = WorkLocation.objects.filter(organization=org)
            self.fields['team'].queryset = Team.objects.filter(organization=org)
            self.fields['direct_manager'].queryset = Employee.objects.filter(organization=org)

class EmployeeUpdateForm(EmployeeCreateForm):
    pass

class EmployeeBankDetailForm(BaseStyledForm):
    class Meta:
        model = EmployeeBankDetail
        fields = ['bank_name', 'account_number', 'account_holder_name', 'ifsc_swift_code', 'branch_name', 'account_type']

class EmployeeTaxInfoForm(BaseStyledForm):
    class Meta:
        model = EmployeeTaxInfo
        fields = ['pan_ssn_number', 'tax_regime', 'pf_uan_number', 'esic_number', 'is_tax_exempt']

class EmergencyContactForm(BaseStyledForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone_number', 'alternate_phone', 'email', 'address', 'is_primary']

class EmployeeAddressForm(BaseStyledForm):
    class Meta:
        model = EmployeeAddress
        fields = ['address_type', 'address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code']

class EmployeeLifecycleTransitionForm(BaseStyledForm):
    class Meta:
        model = EmployeeLifecycleTransition
        fields = ['to_status', 'reason', 'remarks']

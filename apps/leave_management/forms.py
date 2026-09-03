from django import forms
from .models import LeaveType, LeaveApplication

class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name', 'code', 'annual_quota', 'accrual_frequency', 'max_carry_forward_days', 'is_encashable', 'is_unpaid', 'requires_attachment', 'color_hex', 'description']
        widgets = {
            'color_hex': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['leave_type', 'start_date', 'end_date', 'session', 'reason', 'contact_details', 'attachment']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['leave_type'].queryset = self.fields['leave_type'].queryset.filter(organization=org)

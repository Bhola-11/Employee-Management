from django import forms
from .models import EmployeeOnboarding, OnboardingTask, EmployeeOffboarding, OffboardingClearance

class EmployeeOnboardingForm(forms.ModelForm):
    class Meta:
        model = EmployeeOnboarding
        fields = ['employee', 'template', 'start_date', 'target_completion_date', 'buddy', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'target_completion_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['employee'].queryset = self.fields['employee'].queryset.filter(organization=org)
            self.fields['template'].queryset = self.fields['template'].queryset.filter(organization=org)
            self.fields['buddy'].queryset = self.fields['buddy'].queryset.filter(organization=org)


class OnboardingTaskUpdateForm(forms.ModelForm):
    class Meta:
        model = OnboardingTask
        fields = ['status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }


class EmployeeOffboardingForm(forms.ModelForm):
    class Meta:
        model = EmployeeOffboarding
        fields = ['employee', 'notice_date', 'last_working_day', 'reason', 'detailed_reason', 'handover_to']
        widgets = {
            'notice_date': forms.DateInput(attrs={'type': 'date'}),
            'last_working_day': forms.DateInput(attrs={'type': 'date'}),
            'detailed_reason': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['employee'].queryset = self.fields['employee'].queryset.filter(organization=org)
            self.fields['handover_to'].queryset = self.fields['handover_to'].queryset.filter(organization=org)


class OffboardingClearanceForm(forms.ModelForm):
    class Meta:
        model = OffboardingClearance
        fields = ['status', 'recoverable_amount', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
        }

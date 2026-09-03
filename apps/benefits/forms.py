from django import forms
from .models import BenefitPlan, EmployeeBenefitEnrollment

class BenefitPlanForm(forms.ModelForm):
    class Meta:
        model = BenefitPlan
        fields = ['name', 'code', 'category', 'provider_name', 'employer_monthly_contribution', 'employee_monthly_contribution', 'coverage_amount', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class EmployeeBenefitEnrollmentForm(forms.ModelForm):
    class Meta:
        model = EmployeeBenefitEnrollment
        fields = ['plan', 'nominee_name', 'nominee_relationship']

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['plan'].queryset = self.fields['plan'].queryset.filter(organization=org)

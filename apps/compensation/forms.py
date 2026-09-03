from django import forms
from .models import SalaryBand, SalaryComponent

class SalaryBandForm(forms.ModelForm):
    class Meta:
        model = SalaryBand
        fields = ['job_level', 'name', 'code', 'min_base_salary', 'mid_base_salary', 'max_base_salary', 'currency', 'target_annual_bonus_percentage']

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['job_level'].queryset = self.fields['job_level'].queryset.filter(organization=org)

class SalaryComponentForm(forms.ModelForm):
    class Meta:
        model = SalaryComponent
        fields = ['name', 'code', 'component_type', 'calculation_type', 'percentage_value', 'is_taxable', 'is_statutory', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

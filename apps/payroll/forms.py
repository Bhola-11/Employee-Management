from django import forms
from .models import PayrollRun, EmployeeSalaryStructure

class PayrollRunForm(forms.ModelForm):
    class Meta:
        model = PayrollRun
        fields = ['name', 'year', 'month', 'payroll_cycle', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['payroll_cycle'].queryset = self.fields['payroll_cycle'].queryset.filter(organization=org)


class EmployeeSalaryStructureForm(forms.ModelForm):
    class Meta:
        model = EmployeeSalaryStructure
        fields = ['annual_ctc', 'monthly_gross', 'basic_pay_monthly', 'hra_monthly', 'special_allowance_monthly', 'provident_fund_monthly', 'professional_tax_monthly', 'effective_from']
        widgets = {
            'effective_from': forms.DateInput(attrs={'type': 'date'}),
        }

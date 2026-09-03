from django import forms
from .models import ShiftType, ShiftRoster, ShiftSwapRequest

class ShiftTypeForm(forms.ModelForm):
    class Meta:
        model = ShiftType
        fields = ['name', 'code', 'start_time', 'end_time', 'grace_period_minutes', 'break_duration_minutes', 'is_night_shift', 'half_day_minimum_hours', 'full_day_minimum_hours']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ShiftRosterForm(forms.ModelForm):
    class Meta:
        model = ShiftRoster
        fields = ['employee', 'shift_type', 'date', 'is_weekly_off']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['employee'].queryset = self.fields['employee'].queryset.filter(organization=org)
            self.fields['shift_type'].queryset = self.fields['shift_type'].queryset.filter(organization=org)

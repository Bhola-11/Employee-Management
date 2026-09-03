from django import forms
from .models import AttendanceRecord, AttendanceRegularization

class AttendanceRegularizationForm(forms.ModelForm):
    class Meta:
        model = AttendanceRegularization
        fields = ['requested_clock_in', 'requested_clock_out', 'reason', 'detailed_explanation']
        widgets = {
            'requested_clock_in': forms.TimeInput(attrs={'type': 'time'}),
            'requested_clock_out': forms.TimeInput(attrs={'type': 'time'}),
            'detailed_explanation': forms.Textarea(attrs={'rows': 3}),
        }

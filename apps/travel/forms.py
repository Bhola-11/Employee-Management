from django import forms
from .models import TravelRequisition

class TravelRequisitionForm(forms.ModelForm):
    class Meta:
        model = TravelRequisition
        fields = ['purpose', 'origin_city', 'destination_city', 'departure_date', 'return_date', 'estimated_budget', 'advance_amount_requested', 'description']
        widgets = {
            'departure_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

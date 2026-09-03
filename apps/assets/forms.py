from django import forms
from .models import Asset, AssetCategory

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['category', 'asset_tag', 'name', 'serial_number', 'model_number', 'purchase_date', 'purchase_cost', 'warranty_expiry_date', 'status', 'assigned_to', 'specifications']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'warranty_expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'specifications': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['category'].queryset = self.fields['category'].queryset.filter(organization=org)
            self.fields['assigned_to'].queryset = self.fields['assigned_to'].queryset.filter(organization=org)

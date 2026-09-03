from django import forms
from .models import CompanyDocument, DocumentCategory

class CompanyDocumentForm(forms.ModelForm):
    class Meta:
        model = CompanyDocument
        fields = ['category', 'title', 'version', 'access_level', 'file_attachment', 'effective_date', 'description', 'is_mandatory_acknowledgement']
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['category'].queryset = self.fields['category'].queryset.filter(organization=org)

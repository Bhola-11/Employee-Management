from django import forms
from .models import HelpdeskTicket, TicketComment

class HelpdeskTicketForm(forms.ModelForm):
    class Meta:
        model = HelpdeskTicket
        fields = ['category', 'subject', 'priority', 'description', 'attachment']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['category'].queryset = self.fields['category'].queryset.filter(organization=org)

class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write response or update ticket...'}),
        }

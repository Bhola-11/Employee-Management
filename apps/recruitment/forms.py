from django import forms
from .models import JobRequisition, Candidate, JobApplication, InterviewSchedule, InterviewFeedback, JobOffer

class JobRequisitionForm(forms.ModelForm):
    class Meta:
        model = JobRequisition
        fields = [
            'title', 'code', 'department', 'branch', 'job_level', 'employment_type',
            'number_of_openings', 'status', 'experience_level', 'min_salary', 'max_salary',
            'target_hire_date', 'hiring_manager', 'lead_recruiter', 'description', 'requirements', 'benefits', 'is_published'
        ]
        widgets = {
            'target_hire_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'benefits': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if org:
            self.fields['department'].queryset = self.fields['department'].queryset.filter(organization=org)
            self.fields['branch'].queryset = self.fields['branch'].queryset.filter(organization=org)
            self.fields['job_level'].queryset = self.fields['job_level'].queryset.filter(organization=org)
            self.fields['employment_type'].queryset = self.fields['employment_type'].queryset.filter(organization=org)
            self.fields['hiring_manager'].queryset = self.fields['hiring_manager'].queryset.filter(organization=org)
            self.fields['lead_recruiter'].queryset = self.fields['lead_recruiter'].queryset.filter(organization=org)


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'current_company',
            'current_designation', 'total_experience_years', 'current_ctc',
            'expected_ctc', 'notice_period_days', 'source', 'referred_by',
            'resume_file', 'linkedin_url', 'portfolio_url', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class InterviewScheduleForm(forms.ModelForm):
    class Meta:
        model = InterviewSchedule
        fields = ['title', 'interviewers', 'scheduled_start', 'scheduled_end', 'meeting_link', 'location_room', 'status', 'instructions']
        widgets = {
            'scheduled_start': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'scheduled_end': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }


class InterviewFeedbackForm(forms.ModelForm):
    class Meta:
        model = InterviewFeedback
        fields = ['technical_score', 'communication_score', 'culture_fit_score', 'overall_score', 'recommendation', 'pros', 'cons', 'summary_comments']
        widgets = {
            'pros': forms.Textarea(attrs={'rows': 3}),
            'cons': forms.Textarea(attrs={'rows': 3}),
            'summary_comments': forms.Textarea(attrs={'rows': 4}),
        }


class JobOfferForm(forms.ModelForm):
    class Meta:
        model = JobOffer
        fields = ['offered_salary', 'variable_bonus', 'sign_on_bonus', 'joining_date', 'offer_expiry_date', 'status', 'special_terms', 'offer_letter_document']
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'offer_expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'special_terms': forms.Textarea(attrs={'rows': 3}),
        }

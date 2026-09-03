from django import forms
from .models import GoalObjective, EmployeeAppraisal

class GoalObjectiveForm(forms.ModelForm):
    class Meta:
        model = GoalObjective
        fields = ['title', 'category', 'target_date', 'progress_percentage', 'priority', 'status', 'key_metric', 'description']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SelfAppraisalForm(forms.ModelForm):
    class Meta:
        model = EmployeeAppraisal
        fields = ['self_achievements', 'self_areas_for_growth', 'self_rating']
        widgets = {
            'self_achievements': forms.Textarea(attrs={'rows': 4}),
            'self_areas_for_growth': forms.Textarea(attrs={'rows': 3}),
        }

class ManagerAppraisalForm(forms.ModelForm):
    class Meta:
        model = EmployeeAppraisal
        fields = ['manager_feedback', 'manager_rating', 'final_score', 'promotion_recommended', 'recommended_bonus_percentage']
        widgets = {
            'manager_feedback': forms.Textarea(attrs={'rows': 4}),
        }

from django import forms
from .models import Course, CourseModule

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'code', 'category', 'level', 'duration_hours', 'instructor_name', 'description', 'is_mandatory', 'thumbnail']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

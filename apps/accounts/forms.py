from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm
from .models import User, Role, UserRoleAssignment
from apps.organizations.models import Organization

class BaseStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label or field_name.replace('_', ' ').title()

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@company.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user = authenticate(username=email, password=password)
            if not self.user:
                raise forms.ValidationError('Invalid email or password.')
            if not self.user.is_active:
                raise forms.ValidationError('This account has been deactivated.')
        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)

class UserProfileForm(BaseStyledForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'avatar', 'dark_mode', 'preferred_language']

class UserCreateForm(BaseStyledForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ModelChoiceField(queryset=Role.objects.filter(is_active=True), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'is_org_admin']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

class UserRoleAssignmentForm(forms.ModelForm):
    class Meta:
        model = UserRoleAssignment
        fields = ['role', 'department', 'is_primary']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

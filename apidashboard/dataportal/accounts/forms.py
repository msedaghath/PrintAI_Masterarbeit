from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    """Form for user profile management"""
    class Meta:
        model = Profile
        fields = ['name', 'email', 'organization']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'organization': forms.TextInput(attrs={'class': 'form-control'})
        }
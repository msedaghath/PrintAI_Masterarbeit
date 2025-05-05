from django import forms
from .models import Printer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ['ip_address', 'api_key']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UploadGcodeForm(forms.Form):
    gcode = forms.FileField()

# ProfileForm removed as we're using User model directly


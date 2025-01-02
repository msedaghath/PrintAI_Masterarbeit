from django import forms
from .models import DataPrint
from .models import Printer
from .models import Profile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DataPrintForm(forms.ModelForm):
    class Meta:
        model = DataPrint
        fields = ['location', 'data', 'print_date' ]

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username' , 'organization']


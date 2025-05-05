from django import forms
from .models import Printer

class PrinterForm(forms.ModelForm):
    """Form for printer creation and management"""
    class Meta:
        model = Printer
        fields = ['ip_address', 'api_key']
        widgets = {
            'ip_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IP Address or URL'}),
            'api_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'API Key'})
        }
        labels = {
            'ip_address': 'Printer IP Address or URL',
            'api_key': 'OctoPrint API Key'
        }
        help_texts = {
            'ip_address': 'Enter the IP address or URL of your OctoPrint server (e.g., 192.168.1.100 or http://octopi.local)',
            'api_key': 'Enter your OctoPrint API key from Settings > API > API Key'
        }
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import ipaddress
from urllib.parse import urlparse

# Validate IP address or URL
def validate_ip_or_url(value):
    try:
        ipaddress.ip_address(value)
    except ValueError:
        try:
            result = urlparse(value)
            if not all([result.scheme, result.netloc]):
                raise ValueError
        except ValueError:
            raise ValidationError(f"'{value}' is not a valid IP address or URL.")
        
# Removing the Profile model and directly using User model

class Printer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='portal_printers')
    ip_address = models.CharField(max_length=255, validators=[validate_ip_or_url])
    api_key = models.CharField(max_length=32)
    id = models.AutoField(primary_key=True)
    ping = models.BooleanField(default=False)
    printing = models.BooleanField(default=False)
    
    class Meta:
        unique_together = (('ip_address', 'api_key'),)
        
    def __str__(self):
        return f"{self.ip_address} ({self.id})"





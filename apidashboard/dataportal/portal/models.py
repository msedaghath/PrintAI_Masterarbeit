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
        
#Models are here 
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    # password = models.CharField(max_length=200, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    # level = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return str(self.username)

class Printer(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.CharField(max_length=255, validators=[validate_ip_or_url])
    api_key = models.CharField(max_length=32)
    id = models.AutoField(primary_key=True)
    ping = models.BooleanField(default=False)
    printing = models.BooleanField(default=False)
    class Meta:
        unique_together = (('ip_address', 'api_key'),)
    




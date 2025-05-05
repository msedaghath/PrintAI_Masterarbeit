from django.db import models
from accounts.models import Profile
from core.validators import validate_ip_or_url

class Printer(models.Model):
    """Model representing a 3D printer connected via OctoPrint"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.CharField(max_length=255, validators=[validate_ip_or_url])
    api_key = models.CharField(max_length=32)
    id = models.AutoField(primary_key=True)
    ping = models.BooleanField(default=False)
    printing = models.BooleanField(default=False)
    
    class Meta:
        unique_together = (('ip_address', 'api_key'),)
    
    def __str__(self):
        return f"{self.ip_address} ({self.id})"
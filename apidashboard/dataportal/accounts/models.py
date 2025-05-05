from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """User profile model extending Django's built-in User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='accounts_profile')
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    organization = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return str(self.username or self.user.username)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from printers.models import Printer
from accounts.models import Profile

@login_required(login_url='login')
def dashboard(request):
    """Central dashboard view displaying an overview of the system"""
    # Get user profile and their printers
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    printers = Printer.objects.filter(profile=user_profile)
    
    # Count online printers
    online_printers = printers.filter(ping=True).count()
    
    context = {
        'printers': printers,
        'printer_count': printers.count(),
        'online_printers': online_printers,
    }
    
    return render(request, 'core/dashboard.html', context)

class SystemHealthView(LoginRequiredMixin, View):
    """View for checking system health"""
    login_url = 'login'
    
    def get(self, request):
        # Check system services health
        # This is a placeholder for actual health checks
        services = {
            'prometheus': True,
            'grafana': True,
            'octoprint': True
        }
        
        return render(request, 'core/system_health.html', {'services': services})
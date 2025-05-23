"""dataportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # Main dashboard index - redirect to core dashboard
    path('', lambda request: redirect('dashboard') if request.user.is_authenticated else redirect('login'), name='index'),
    # Include app URLs
    path('dashboard/', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('printers/', include('printers.urls')),
    path('monitoring/', include('monitoring.urls')),
    path('api/', include('api.urls')),
    # Legacy routes - keep temporarily until migration is complete
    path('portal/', include('portal.urls')),
]

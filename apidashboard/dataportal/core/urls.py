from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('system-health/', views.SystemHealthView.as_view(), name='system_health'),
]